import logging
from uuid import UUID
from app.repositories.question_repository import QuestionRepository
from app.v1.modules.question.dto.question_create_dto import QuestionCreateDTO
from app.v1.modules.question.dto.question_dto import QuestionDTO
from app.models.question import Question
from app.v1.modules.question.services.question_service import QuestionService


logger = logging.getLogger(__name__)


class QuestionImplService(QuestionService):
    """
    Concrete implementation of the QuestionService.

    Handles the business logic required to create and manage
    learning questions while delegating persistence operations
    to the QuestionRepository.
    """

    def __init__(
        self,
        question_repository: QuestionRepository,
    ):
        self.question_repository = question_repository


    async def get_questions_count_by_topic(
        self,
        topic_id: UUID,
    ) -> int:
        """
        Return the number of active questions belonging
        to a specific learning topic.

        The actual database query remains inside the
        QuestionRepository. This service exposes the
        question-related operation to other services
        without allowing them to directly access the
        question data layer.

        Args:
            topic_id:
                Identifier of the learning topic.

        Returns:
            Number of active questions available for
            the specified topic.
        """

        return (
            await self.question_repository
            .count_by_topic_id(topic_id)
        )

    # ============================================================
    # CREATE
    # ============================================================
    async def create_question(
        self,
        question_data: QuestionCreateDTO,
    ) -> QuestionDTO:
        """
        Create and persist a new learning question.

        The question is created from the validated DTO and
        persisted through the QuestionRepository.

        Args:
            question_data:
                Validated data required to create the question.

        Returns:
            The newly created Question entity.

        Raises:
            Exception:
                Propagates persistence or business errors so they
                can be handled by the application's exception layer.
        """
        try:
            question = Question(
                **question_data.model_dump()
            )

            await self.question_repository.add(question)

            return QuestionDTO.model_validate(question)

        except Exception:
            logger.exception(
                "Error creating question",
            )
            raise