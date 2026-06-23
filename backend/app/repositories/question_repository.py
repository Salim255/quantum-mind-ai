from app.repositories.base_repository import BaseRepository
from app.models.question import Question
from sqlmodel import Session

class QuestionRepository(BaseRepository[Question]):
    """
    Repository for question database queries.

    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session: Session):
        super().__init__(session, Question)