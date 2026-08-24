from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.attempt_repository import AttemptRepository
from app.v1.modules.question.dependencies import get_question_service
from app.v1.modules.question.services.question_service import QuestionService
from app.v1.modules.attempt.services.attempt_impl_service import (
    AttemptImplService,
)
from app.v1.modules.attempt.services.attempt_service import (
    AttemptService,
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
# ATTEMPT REPOSITORY DEPENDENCY
# ============================================================

def get_attempt_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> AttemptRepository:
    """
    Create the AttemptRepository for the current request.

    The repository is responsible exclusively for data access
    related to Attempt entities.

    Args:
        session:
            Active asynchronous database session.

    Returns:
        An AttemptRepository bound to the current database session.
    """
    return AttemptRepository(session)


# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_attempt_service(
    attempt_repository: Annotated[
        AttemptRepository,
        Depends(get_attempt_repository),
    ],
    question_service: Annotated[
        QuestionService,
        Depends(get_question_service),
    ],
) -> AttemptService:
    """
    Create the AttemptService for the current request.

    The AttemptService coordinates attempt-related business logic.

    It uses:
    - AttemptRepository for attempt persistence.
    - QuestionService for question-related operations.

    Keeping question operations behind QuestionService prevents
    the AttemptService from depending directly on the QuestionRepository.

    Args:
        attempt_repository:
            Repository responsible for Attempt persistence.

        question_service:
            Service responsible for question-related business logic.

    Returns:
        The concrete AttemptService implementation.
    """
    return AttemptImplService(
        attempt_repository=attempt_repository,
        question_service=question_service,
    )