from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.attempt_question_repository import (
    AttemptQuestionRepository,
)
from app.v1.modules.attempt_question.services.attempt_question_impl_service import (
    AttemptQuestionImplService,
)
from app.v1.modules.attempt_question.services.attempt_question_service import (
    AttemptQuestionService,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieve the application dependency container.
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
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# REPOSITORY DEPENDENCY
# ============================================================

def get_attempt_question_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> AttemptQuestionRepository:
    """
    Create the AttemptQuestionRepository for the current request.
    """

    return AttemptQuestionRepository(session)


# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_attempt_question_service(
    attempt_question_repository: Annotated[
        AttemptQuestionRepository,
        Depends(get_attempt_question_repository),
    ],
) -> AttemptQuestionService:
    """
    Create the AttemptQuestionService for the current request.
    """

    return AttemptQuestionImplService(
        attempt_question_repository=attempt_question_repository,
    )