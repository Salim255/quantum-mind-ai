from abc import ABC, abstractmethod
from uuid import UUID
from app.v1.modules.question.dto.question_create_dto import QuestionCreateDTO
from app.v1.modules.question.dto.question_dto import QuestionDTO


class QuestionService(ABC):
    """
    Service contract for managing learning questions.

    Defines the business operations available for questions while
    keeping the controller independent from the concrete service
    implementation.

    The concrete implementation is responsible for coordinating
    repositories and enforcing question-related business rules.
    """


    async def get_questions_count_by_topic(
        self,
        topic_id: UUID,
    ) -> int:
        """
        Return the number of active questions available
        for a specific learning topic.

        This method is primarily used by other application
        services, such as AttemptService, when they need
        question-related information without directly
        accessing the QuestionRepository.
        """
        raise NotImplementedError(
            "get_questions_count_by_topic() must be implemented"
        )

    # ============================================================
    # CREATE
    # ============================================================
    @abstractmethod
    async def create_question(
        self,
        question_data: QuestionCreateDTO,
    ) -> QuestionDTO:
        """
        Create a new learning question.

        A question must belong to an existing Topic.

        The service is responsible for validating the required
        business rules before persisting the question.

        Args:
            question_data:
                Data required to create the question.

        Returns:
            The newly created Question entity.
        """
        raise NotImplementedError(
            "create_question() must be implemented"
        )