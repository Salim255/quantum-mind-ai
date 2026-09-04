from sqlmodel.ext.asyncio.session import AsyncSession

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
# SERVICE DEPENDENCY
# ============================================================

def get_attempt_question_service(
    session: AsyncSession
) -> AttemptQuestionService:
    """
    Create the AttemptQuestionService for the current request.
    """

    attempt_question_repository = AttemptQuestionRepository(session=session)
    return AttemptQuestionImplService(
        attempt_question_repository=attempt_question_repository,
    )