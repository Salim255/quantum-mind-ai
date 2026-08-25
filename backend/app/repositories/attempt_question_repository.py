from app.models.attempt_question import AttemptQuestion
from app.repositories.base_repository import BaseRepository
from sqlmodel import Session


class AttemptQuestionRepository(
    BaseRepository[AttemptQuestion]
):
    """
    Repository for attempt question database queries.

    Inherits common CRUD operations from BaseRepository.

    The repository is responsible for data access related to
    individual questions presented during quiz attempts.
    """

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(
            session,
            AttemptQuestion,
        )