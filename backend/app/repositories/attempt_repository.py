from app.repositories.base_repository import BaseRepository
from app.models.attempt import Attempt
from sqlmodel import Session

class AttemptRepository(BaseRepository[Attempt]):
    """
    Repository for quiz_attempts database queries.

    Inherits common CRUD operations from BaseRepository.
    """
     
    def __init__(self, session: Session):
        super().__init__(session, Attempt)