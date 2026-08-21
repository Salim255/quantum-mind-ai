from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.answer_repository import AnswerRepository
from app.v1.modules.answer.services.answer_impl_service import (
    AnswerImplService,
)
from app.v1.modules.answer.services.answer_service import (
    AnswerService,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieve the application dependency container.

    The container owns application-wide dependencies such as:
    - database session management
    - repositories
    - external service clients
    - shared infrastructure services

    Args:
        request:
            Current FastAPI request.

    Returns:
        The application's dependency container.
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
    Provide an asynchronous database session.

    The session is created by the application's database session
    manager and injected into repositories.

    Important:
        This dependency yields the actual AsyncSession.
        It does not expose the DB session manager itself.

    Args:
        container:
            Application dependency container.

    Yields:
        An active asynchronous database session.
    """
    async for session in container.db_session.get_session():
        yield session


# ============================================================
# REPOSITORY DEPENDENCY
# ============================================================

def get_answer_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> AnswerRepository:
    """
    Create the AnswerRepository for the current request.

    The repository is responsible exclusively for data access,
    including querying and persisting Answer entities.

    Args:
        session:
            Active asynchronous database session.

    Returns:
        An AnswerRepository bound to the current database session.
    """
    return AnswerRepository(session)


# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_answer_service(
    answer_repository: Annotated[
        AnswerRepository,
        Depends(get_answer_repository),
    ],
) -> AnswerService:
    """
    Create the AnswerService for the current request.

    The service contains answer-related business logic and
    delegates persistence operations to the repository.

    Args:
        answer_repository:
            Answer repository for the current request.

    Returns:
        The concrete AnswerService implementation.
    """
    return AnswerImplService(
        answer_repository,
    )

