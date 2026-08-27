from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.v1.modules.auth.services.cookie_impl_service import CookieImplService
from app.v1.modules.auth.services.cookie_service import CookieService

from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_security_repository import UserSecurityRepository
from app.repositories.user_session_repository import UserSessionRepository

from app.v1.modules.auth.services.auth_impl_service import AuthImplService
from app.v1.modules.auth.services.auth_service import AuthService

from app.v1.modules.auth.services.password_impl_service import PasswordImplService
from app.v1.modules.auth.services.password_service import PasswordService
from app.v1.modules.auth.services.jwt_manager_service import JWTManagerService
from app.v1.modules.auth.services.jwt_manager_impl_service import JWTManagerImplService

# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container owns application-wide dependencies such as:

    - application settings
    - database session management
    - shared security services
    - external clients
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

    All repositories participating in the same authentication
    operation receive the same AsyncSession.
    """

    async for session in container.db_session.get_session():
        yield session

# ============================================================
# PASSWORD SERVICE DEPENDENCY
# ============================================================

def get_password_service() -> PasswordService:
    """
    Provides the shared PasswordService.

    PasswordService is created and owned by the application
    container.

    Authentication depends only on the PasswordService
    abstraction and does not know about the concrete hashing
    implementation.
    """

    return PasswordImplService()


# ============================================================
# JWT MANAGER DEPENDENCY
# ============================================================

def get_jwt_manager_service(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> JWTManagerService:
    """
    Provides the shared JWTManagerService.

    JWTManagerService is created by the application container
    using the application's Settings.

    Authentication therefore does not need direct access to:

    - Settings
    - JWT secret
    - JWT algorithm
    - PyJWT
    """

    return JWTManagerImplService(settings=container.settings)


# ============================================================
# COOKIE SERVICE DEPENDENCY
# ============================================================

def get_cookie_service(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> CookieService:
    """
    Provides the shared CookieService.

    CookieService is initialized by the application container
    with the application's Settings instance.

    The authentication layer therefore does not need direct
    access to Settings for cookie management.
    """

    return CookieImplService(settings=container.settings)


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

    Responsible for user account persistence.
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
    - security timestamps
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

    Responsible for authenticated session persistence and
    session lifecycle management.
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

    Used during registration to create the initial user profile.
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
    profile_repository: Annotated[
        ProfileRepository,
        Depends(get_profile_repository),
    ],
    cookie_service: Annotated[
        CookieService,
        Depends(get_cookie_service),
    ],
    jwt_service: Annotated[
        JWTManagerService, Depends(get_jwt_manager_service)
    ],
    password_service: Annotated [
        PasswordService, Depends(get_password_service)
    ]
) -> AuthService:
    """
    Creates the authentication service.

    AuthService coordinates the authentication workflow while
    delegating persistence and infrastructure responsibilities
    to specialized components.

    Dependencies:

    UserRepository
        User account persistence.

    UserSecurityRepository
        Authentication security state.

    UserSessionRepository
        Authenticated session lifecycle.

    ProfileRepository
        User profile creation during registration.

    CookieService
        Authentication cookie management.
    """

    return AuthImplService(
        user_repository=user_repository,
        user_security_repository=user_security_repository,
        user_session_repository=user_session_repository,
        profile_repository=profile_repository,
        cookie_service=cookie_service,
        jwt_service=jwt_service,
        password_service=password_service
    )