from abc import ABC, abstractmethod

from app.v1.modules.question.dto.question_create_dto import QuestionCreateDTO
from app.v1.modules.question.dto.question_dto import QuestionDto


class QuestionService(ABC):
    """
    Service contract for managing learning questions.

    Defines the business operations available for questions while
    keeping the controller independent from the concrete service
    implementation.

    The concrete implementation is responsible for coordinating
    repositories and enforcing question-related business rules.
    """

    # ============================================================
    # CREATE
    # ============================================================

    @abstractmethod
    async def create_question(
        self,
        question_data: QuestionCreateDTO,
    ) -> QuestionDto:
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