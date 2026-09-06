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
# SERVICE DEPENDENCY
# ============================================================

def get_answer_service(
    session: AsyncSession
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

    answer_repository = AnswerRepository(session)

    return AnswerImplService(
        answer_repository,
    )

