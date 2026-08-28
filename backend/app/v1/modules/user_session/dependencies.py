from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container

from app.repositories.user_session_repository import (
    UserSessionRepository,
)

from app.v1.modules.user_session.services.user_session_service import (
    UserSessionService,
)

from app.v1.modules.user_session.services.user_session_impl_service import (
    UserSessionImplService,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container provides access to application-wide
    infrastructure and shared dependencies.
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

    The session is shared across all repositories involved
    in the same request.
    """

    async for session in container.db_session.get_session():
        yield session


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
    Creates the user session repository.

    Responsible for persistence operations related to
    authenticated user sessions.
    """

    return UserSessionRepository(session)


# ============================================================
# USER SESSION SERVICE
# ============================================================

def get_user_session_service(
    user_session_repository: Annotated[
        UserSessionRepository,
        Depends(get_user_session_repository),
    ],
) -> UserSessionService:
    """
    Creates the user session service.

    UserSessionService coordinates authenticated session
    operations while delegating persistence responsibilities
    to UserSessionRepository.

    Dependencies:

    UserSessionRepository
        Provides persistence operations for authenticated
        user sessions.
    """

    return UserSessionImplService(
        user_session_repository=user_session_repository,
    )