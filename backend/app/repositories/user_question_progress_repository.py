from app.models.user_question_progress import UserQuestionProgress
from app.repositories.base_repository import BaseRepository
from sqlmodel import Session


class UserQuestionProgressRepository(
    BaseRepository[UserQuestionProgress]
):
    """
    Repository for user question progress database queries.

    Inherits common CRUD operations from BaseRepository.

    The repository is responsible for data access related to a
    user's long-term learning progress for individual questions.
    """

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session,
            UserQuestionProgress,
        )