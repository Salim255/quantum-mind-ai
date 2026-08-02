from sqlmodel import Session
from app.models.section import Section
from app.repositories.base_repository import BaseRepository

class SectionRepository(BaseRepository, [Section]):
    def __init__(self, session: Session):
        # Pass Section model to BaseRepository
        super().__init__(session, Section) 