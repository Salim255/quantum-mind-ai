from abc import ABC, abstractmethod
from uuid import UUID

from app.v1.modules.user_question_progress.dto.user_question_progress_create_dto import (
    UserQuestionProgressCreateDTO,
)
from app.v1.modules.user_question_progress.dto.user_question_progress_dto import (
    UserQuestionProgressDTO,
)


class UserQuestionProgressService(ABC):
    """
    Service responsible for business operations related to
    user progress on individual questions.
    """

    @abstractmethod
    async def create_progress(
        self,
        progress_data: UserQuestionProgressCreateDTO,
    ) -> UserQuestionProgressDTO:
        """
        Create a progress record for a user and question.

        Args:
            progress_data:
                Data required to initialize the progress record.

        Returns:
            The created user question progress.
        """
        raise NotImplementedError