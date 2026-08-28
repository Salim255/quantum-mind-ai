from typing import Annotated
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_security_repository import (
    UserSecurityRepository,
)
from app.core.container import Container
from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)

from app.v1.modules.user_security.services.user_security_impl_service import (
    UserSecurityImplService,
)



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
# USER SECURITY SERVICE
# ============================================================

def get_user_security_service(
    user_security_repository: Annotated[
        UserSecurityRepository,
        Depends(get_user_security_repository),
    ],
) -> UserSecurityService:
    """
    Creates the user security service.

    UserSecurityService coordinates authentication security
    state while delegating persistence responsibilities to
    UserSecurityRepository.

    Dependencies:

    UserSecurityRepository
        Provides persistence operations for authentication
        security state.
    """

    return UserSecurityImplService(
        user_security_repository=user_security_repository,
    )
