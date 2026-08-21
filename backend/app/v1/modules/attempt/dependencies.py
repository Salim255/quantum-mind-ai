from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.attempt_repository import AttemptRepository
from app.repositories.question_repository import QuestionRepository
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
# QUESTION REPOSITORY DEPENDENCY
# ============================================================

def get_question_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> QuestionRepository:
    """
    Create the QuestionRepository for the current request.

    The AttemptService uses this repository to resolve the
    questions belonging to the topic when creating an attempt.

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

def get_attempt_service(
    attempt_repository: Annotated[
        AttemptRepository,
        Depends(get_attempt_repository),
    ],
    question_repository: Annotated[
        QuestionRepository,
        Depends(get_question_repository),
    ],
) -> AttemptService:
    """
    Create the AttemptService for the current request.

    The service coordinates both repositories because creating
    an attempt requires resolving the questions associated with
    the selected topic.

    Args:
        attempt_repository:
            Repository responsible for Attempt persistence.

        question_repository:
            Repository responsible for retrieving the topic's
            questions.

    Returns:
        The concrete AttemptService implementation.
    """
    return AttemptImplService(
        attempt_repository=attempt_repository,
        question_repository=question_repository,
    )