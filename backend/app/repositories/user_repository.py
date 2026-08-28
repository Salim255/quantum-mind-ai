
from sqlmodel import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository
from typing import Generic, TypeVar, Type, Optional, List
from sqlmodel import select

T = TypeVar("T")

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        # Pass Block model to BaseRepository
        super().__init__(session, User)

        # --------------------------------------------------
    # GET BY USER ID
    # --------------------------------------------------
    async def get_by_user_email(
        self,
        email: str
    ) -> Optional[T]:
        """
        Fetch one entity by user id.
        """

        statement = select(User).where(
            User.email == email
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()
