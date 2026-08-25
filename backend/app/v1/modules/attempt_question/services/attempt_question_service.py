from abc import ABC, abstractmethod
from uuid import UUID

from app.v1.modules.attempt_question.dto.attempt_question_create_dto import (
    AttemptQuestionCreateDTO,
)
from app.v1.modules.attempt_question.dto.attempt_question_dto import (
    AttemptQuestionDTO,
)


class AttemptQuestionService(ABC):
    """
    Service responsible for business operations related to
    questions presented during quiz attempts.
    """

    @abstractmethod
    async def create_attempt_question(
        self,
        attempt_question_data: AttemptQuestionCreateDTO,
    ) -> AttemptQuestionDTO:
        """
        Create a question instance associated with a quiz attempt.

        Args:
            attempt_question_data:
                Data required to create the attempt question.

        Returns:
            The created attempt question.
        """
        raise NotImplementedError