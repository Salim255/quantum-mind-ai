from typing import Annotated
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container

from app.repositories.user_repository import UserRepository

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