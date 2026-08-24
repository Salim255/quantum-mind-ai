from app.repositories.base_repository import BaseRepository
from app.models.attempt import Attempt
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from uuid import UUID


class AttemptRepository(BaseRepository[Attempt]):
    """
    Repository for quiz_attempts database queries.

    Inherits common CRUD operations from BaseRepository.
    """
     
    def __init__(self, session: Session):
        super().__init__(session, Attempt)


           
    async def get_by_id_with_topic(
        self,
        attempt_id: UUID,
    ) -> Attempt | None:
        statement = (
            select(Attempt)
            .options(
                selectinload(Attempt.topic),
            )
            .where(Attempt.id == attempt_id)
        )

        result = await self.session.execute(statement)

        return result.scalar_one_or_none()