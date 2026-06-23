from app.repositories.base_repository import BaseRepository
from app.models.quiz_attempt import QuizAttempt
from sqlmodel import Session

class QuizAttemptRepository(BaseRepository[QuizAttempt]):
    """
    Repository for quiz_attempts database queries.

    Inherits common CRUD operations from BaseRepository.
    """
     
    def __init__(self, session: Session):
        super().__init__(session, QuizAttempt)