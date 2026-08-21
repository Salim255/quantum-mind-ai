from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.question_repository import QuestionRepository
from app.v1.modules.question.services.question_impl_service import (
    QuestionImplService,
)
from app.v1.modules.question.services.question_service import (
    QuestionService,
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


def get_question_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> QuestionRepository:
    """
    Create the QuestionRepository for the current request.

    The repository is responsible exclusively for data access,
    including querying and persisting Question entities.

    Args:
        session:
            Active asynchronous database session.

    Returns:
        A QuestionRepository bound to the current database session.
    """
    return QuestionRepository(session)


# ============================================================
# SERVICE DEPENDENCY
# ============================================================
def get_question_service(
    question_repository: Annotated[
        QuestionRepository,
        Depends(get_question_repository),
    ],
) -> QuestionService:
    """
    Create the QuestionService for the current request.

    The service contains question-related business logic and
    delegates persistence operations to the repository.

    Args:
        question_repository:
            Question repository for the current request.

    Returns:
        The concrete QuestionService implementation.
    """
    return QuestionImplService(
        question_repository,
    )