
from sqlmodel import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        # Pass Block model to BaseRepository
        super().__init__(session, User)