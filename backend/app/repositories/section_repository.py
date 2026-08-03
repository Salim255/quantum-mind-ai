from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.base_repository import BaseRepository
from app.models.section import Section

class SectionRepository(BaseRepository[Section]):
    def __init__(self, session: AsyncSession):
        # Pass Section model to BaseRepository
        super().__init__(session, Section) 