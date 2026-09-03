from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container
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
# SERVICE DEPENDENCY
# ============================================================

def get_attempt_service(
    session: AsyncSession,
    container: Container,
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

    attempt_repository = AttemptRepository(session=session)
    question_service: QuestionService = get_question_service(
        session=session,
        container=container
    )

    return AttemptImplService(
        attempt_repository=attempt_repository,
        question_service=question_service,
    )