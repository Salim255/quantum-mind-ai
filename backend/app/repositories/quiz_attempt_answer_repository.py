from app.repositories.base_repository import BaseRepository
from app.models.quiz_attempt_answer import QuizAttemptAnswer
from sqlmodel import Session

class QuizAttemptAnswerRepository(BaseRepository[QuizAttemptAnswer]):
    """
    Repository for quiz_attempt_answers database queries.

    Inherits common CRUD operations from BaseRepository.
    """
    def __init__(self, session: Session):
        super().__init__(session, QuizAttemptAnswer)
