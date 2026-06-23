from app.repositories.base_repository import BaseRepository
from app.models.question_option import QuestionOption
from sqlmodel import Session

class QuestionOptionRepository(BaseRepository[QuestionOption]):
    """
    Repository for question_options database queries.

    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session: Session):
        super().__init__(session, QuestionOption)