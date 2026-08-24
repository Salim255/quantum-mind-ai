from fastapi import logger

from app.models.attempt import Attempt
from app.repositories.attempt_repository import AttemptRepository
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.question.services.question_service import QuestionService
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO

class AttemptImplService(AttemptService):
    """
    Concrete implementation of the AttemptService.

    Responsible for creating and initializing learning attempts.

    The service coordinates the AttemptRepository and
    QuestionRepository because an attempt is created from
    the questions belonging to a specific topic.
    """

    def __init__(
        self,
        attempt_repository: AttemptRepository,
        question_service: QuestionService,
    ):
        self.attempt_repository = attempt_repository
        self.question_service = question_service

    # ============================================================
    # CREATE
    # ============================================================

    async def create_attempt(
        self,
        attempt_data: AttemptCreateDTO,
    ) -> AttemptDTO:
        """
        Create and initialize a new learning attempt.

        The questions are resolved from the supplied topic.
        The number of active questions becomes the attempt's
        total_questions value.

        Args:
            attempt_data:
                Validated attempt creation data.

        Returns:
            The newly created Attempt entity.
        """

        try:
            print("hello from count")
            attempt = Attempt(
                user_id=attempt_data.user_id,
                topic_id=attempt_data.topic_id,
                score=0.0,
                total_questions=0,
                correct_answers=0,
                is_completed=False,
            )

            await self.attempt_repository.add(attempt)

            return AttemptDTO.model_validate(attempt)

        except Exception:
            logger.exception("Error creating attempt")
            raise