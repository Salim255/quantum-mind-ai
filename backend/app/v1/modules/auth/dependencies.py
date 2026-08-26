from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container

from app.repositories.user_repository import UserRepository
from app.repositories.user_security_repository import UserSecurityRepository
from app.repositories.user_session_repository import UserSessionRepository
from app.repositories.profile_repository import ProfileRepository

from app.v1.modules.auth.service.auth_service import AuthService
from app.v1.modules.auth.service.auth_impl_service import AuthImplService


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container owns application-wide infrastructure such as:

    - database session management
    - external clients
    - shared services
    - application configuration
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
):
    """
    Provides an asynchronous database session.

    The same session is injected into all repositories used during
    a single authentication operation.

    This is important because registration and authentication may
    involve multiple database operations that should participate
    in the same transaction.
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# USER REPOSITORY
# ============================================================

def get_user_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> UserRepository:
    """
    Creates the UserRepository.

    Authentication uses the repository directly because user
    persistence is part of the authentication workflow.

    Typical operations include:

    - find user by email
    - create user
    - update authentication-related user state
    """

    return UserRepository(session)


# ============================================================
# USER SECURITY REPOSITORY
# ============================================================

def get_user_security_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> UserSecurityRepository:
    """
    Creates the UserSecurityRepository.

    Responsible for persistent authentication security state,
    such as:

    - failed login attempts
    - account lock state
    - password security metadata
    - security version
    - authentication-related timestamps
    """

    return UserSecurityRepository(session)


# ============================================================
# USER SESSION REPOSITORY
# ============================================================

def get_user_session_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> UserSessionRepository:
    """
    Creates the UserSessionRepository.

    Responsible for persistence of authenticated sessions.

    Authentication uses this repository to:

    - create sessions
    - retrieve sessions
    - revoke sessions
    - track session lifecycle
    """

    return UserSessionRepository(session)


# ============================================================
# PROFILE REPOSITORY
# ============================================================

def get_profile_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> ProfileRepository:
    """
    Creates the ProfileRepository.

    Registration may use this repository to create the user's
    initial profile as part of the account-creation transaction.

    Profile-specific operations remain outside UserService and
    AuthService unless they are explicitly part of the
    authentication workflow.
    """

    return ProfileRepository(session)


# ============================================================
# AUTH SERVICE
# ============================================================

def get_auth_service(
    user_repository: Annotated[
        UserRepository,
        Depends(get_user_repository),
    ],
    user_security_repository: Annotated[
        UserSecurityRepository,
        Depends(get_user_security_repository),
    ],
    user_session_repository: Annotated[
        UserSessionRepository,
        Depends(get_user_session_repository),
    ],
    refresh_token_repository: Annotated[
        RefreshTokenRepository,
        Depends(get_refresh_token_repository),
    ],
    profile_repository: Annotated[
        ProfileRepository,
        Depends(get_profile_repository),
    ],
) -> AuthService:
    """
    Creates the authentication service.

    AuthService orchestrates the complete authentication workflow.

    Dependencies:

        UserRepository
            Account identity and credentials.

        UserSecurityRepository
            Authentication security state.

        UserSessionRepository
            Authenticated session lifecycle.

        RefreshTokenRepository
            Refresh-token lifecycle and rotation.

        ProfileRepository
            Initial profile creation during registration.

    All repositories receive the same AsyncSession, allowing the
    authentication workflow to operate within the same database
    transaction.
    """

    return AuthImplService(
        user_repository=user_repository,
        user_security_repository=user_security_repository,
        user_session_repository=user_session_repository,
        refresh_token_repository=refresh_token_repository,
        profile_repository=profile_repository,
    )

