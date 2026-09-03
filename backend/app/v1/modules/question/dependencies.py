from typing import Annotated

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
# SERVICE DEPENDENCY
# ============================================================
def get_question_service(
    session: AsyncSession
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
    question_repository = QuestionRepository(session=session)

    return QuestionImplService(
        question_repository,
    )