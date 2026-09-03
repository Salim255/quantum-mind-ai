import logging
from uuid import UUID
from app.models.attempt import Attempt
from app.repositories.attempt_repository import AttemptRepository
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.question.services.question_service import QuestionService
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO

logger = logging.getLogger(__name__)

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
          
            attempt = Attempt(
                user_id=attempt_data.user_id,
                topic_id=attempt_data.topic_id,
                score=0.0,
                total_questions=(
                    await self.question_service
                    .get_questions_count_by_topic(attempt_data.topic_id)
                ),
                correct_answers=0,
                is_completed=False,
            )

            await self.attempt_repository.add(attempt)

            attempt = await self.attempt_repository.get_by_id_with_topic_questions(
                attempt.id
            )

            return AttemptDTO.model_validate(attempt)

        except Exception:
            logger.exception("Error creating attempt")
            raise


    # ============================================================
    # GET LATEST ATTEMPTS BY TOPIC
    # ============================================================

    async def get_latest_attempt_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID
    ) -> list[AttemptDTO] | None:
        """
        Retrieves the latest attempt for each topic belonging
        to the specified user.

        The repository is responsible for retrieving the
        appropriate attempts from the database.

        The service converts the resulting entities into
        AttemptDTO objects.
        """

        try:

            attempts = (
                await self.attempt_repository
                .get_latest_attempt_by_user_and_topic(
                    user_id=user_id,
                    topic_id=topic_id
                )
            )

            return [
                AttemptDTO.model_validate(attempt)
                for attempt in attempts
            ]

        except Exception:
            logger.exception(
                "Error retrieving latest attempts by topic"
            )
            raise