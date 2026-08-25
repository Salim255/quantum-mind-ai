from app.models.user_question_progress import UserQuestionProgress
from app.repositories.user_question_progress_repository import (
    UserQuestionProgressRepository,
)
from app.v1.modules.user_question_progress.dto.user_question_progress_create_dto import (
    UserQuestionProgressCreateDTO,
)
from app.v1.modules.user_question_progress.dto.user_question_progress_dto import (
    UserQuestionProgressDTO,
)
from app.v1.modules.user_question_progress.services.user_question_progress_service import (
    UserQuestionProgressService,
)
import logging

logger = logging.getLogger(__name__)

class UserQuestionProgressImplService(
    UserQuestionProgressService
):
    """
    Concrete implementation of UserQuestionProgressService.

    Responsible for applying business rules related to a user's
    long-term progress on individual questions.
    """

    def __init__(
        self,
        user_question_progress_repository: UserQuestionProgressRepository,
    ):
        self.user_question_progress_repository = (
            user_question_progress_repository
        )

    async def create_progress(
        self,
        progress_data: UserQuestionProgressCreateDTO,
    ) -> UserQuestionProgressDTO:
        """
        Create and persist a user question progress record.

        A new progress record starts with neutral learning metrics.
        These metrics are updated as the user interacts with the
        question through quiz attempts.

        Args:
            progress_data:
                Data required to create the progress record.

        Returns:
            The persisted progress record as a DTO.
        """

        try:
            progress = UserQuestionProgress(
                        user_id=progress_data.user_id,
                        question_id=progress_data.question_id,
                    )
            
            await self.user_question_progress_repository.add(
                progress
            )
    
            return UserQuestionProgressDTO.model_validate(
                progress
            )
        except Exception:
            logger.exception("Error in create user question progress")
            raise