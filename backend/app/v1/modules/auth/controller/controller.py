from typing import Annotated
from collections.abc import AsyncGenerator

from fastapi import Depends, Request, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.auth.dependencies import get_auth_service
from app.v1.modules.auth.dto.auth_dto import (
    AuthResponseDTO,
    LoginDTO,
    RegisterDTO,
)
from app.v1.modules.auth.services.auth_service import AuthService

from .router import router as auth_router


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container is stored on FastAPI's application state.

    It provides access to application-wide infrastructure such as:

    - application settings
    - database session management
    - shared infrastructure services

    The controller is responsible for obtaining the container
    because it represents the outer application boundary.
    """

    return request.app.state.container


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db_session(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> AsyncGenerator[
    AsyncSession,
    None,
]:
    """
    Provides the database session for the current request.

    The session is created by the database session manager
    owned by the application container.

    IMPORTANT:

    The controller is the boundary where the database session
    enters the application service layer.

    The session is then explicitly passed to the service factory.

    This allows multiple services and repositories to share
    the exact same AsyncSession.
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# REGISTER
# ============================================================

@auth_router.post(
    "/register",
    response_model=ResponseDTO[AuthResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
Creates a new QuantumMind user account.

The registration process is handled by the authentication service.

The service is responsible for:

- validating the registration data
- checking email uniqueness
- hashing the password
- creating the user
- creating the user profile
- creating the user security record
- creating the initial session
- issuing authentication tokens
""",
    responses={
        201: {
            "description": "User successfully registered."
        },
        400: {
            "description": "Invalid registration data."
        },
        409: {
            "description": "An account with the provided email already exists."
        },
    },
)
async def register(
    payload: RegisterDTO,
    response: Response,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AuthResponseDTO]:
    """
    Registers a new user.

    The controller obtains the database session and passes it
    explicitly to the authentication service factory.

    The authentication service then passes the SAME session
    to all database-dependent services.

    Dependency flow:

        FastAPI
          │
          ├── Container
          │
          └── AsyncSession
                  │
                  ▼
          get_auth_service(...)
                  │
                  ├── UserService(session)
                  ├── ProfileService(session)
                  ├── SecurityService(session)
                  ├── SessionService(session)
                  └── UnitOfWork(session)

    Therefore the complete registration workflow can operate
    inside one database transaction.
    """

    # --------------------------------------------------------
    # CREATE AUTH SERVICE
    # --------------------------------------------------------

    # The controller explicitly provides the session.

    auth_service: AuthService = get_auth_service(
        session=session,
        container=container
    )

    # --------------------------------------------------------
    # EXECUTE REGISTRATION
    # --------------------------------------------------------

    return ResponseDTO.success(await auth_service.register(payload, response))


# ============================================================
# LOGIN
# ============================================================

@auth_router.post(
    "/login",
    response_model=ResponseDTO[AuthResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="""
Authenticates an existing QuantumMind user.

The authentication service validates the credentials,
checks the account security state, creates an authenticated
session, and issues the required authentication tokens.
""",
    responses={
        200: {
            "description": "User successfully authenticated."
        },
        401: {
            "description": "Invalid authentication credentials."
        },
        403: {
            "description": "User account is inactive or locked."
        },
    },
)
async def login(
    payload: LoginDTO,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AuthResponseDTO]:
    """
    Authenticates an existing user.

    The same dependency pattern is used as registration:

        Controller
            ↓
        AsyncSession
            ↓
        get_auth_service()
            ↓
        AuthService
            ↓
        database-dependent services

    The session is therefore controlled by the request boundary
    rather than by AuthService itself.
    """

    # --------------------------------------------------------
    # CREATE AUTH SERVICE
    # --------------------------------------------------------

    auth_service: AuthService = get_auth_service(
        session=session,
        container=container,
    )

    # --------------------------------------------------------
    # EXECUTE LOGIN
    # --------------------------------------------------------

    return ResponseDTO.success(
        await auth_service.login(payload)
    )