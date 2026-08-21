from app.repositories.base_repository import BaseRepository
from app.models.answer import Answer
from sqlmodel import Session

class AnswerRepository(BaseRepository[Answer]):
    """
    Repository for question_options database queries.

    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session: Session):
        super().__init__(session, Answer)