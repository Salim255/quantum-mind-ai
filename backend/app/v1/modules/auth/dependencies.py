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
    )