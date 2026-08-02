
from sqlmodel import Session
from app.models.block import Block
from backend.app.repositories.base_repository import BaseRepository


class BlockRepository(BaseRepository, [Block]):
    def __init__(self, session: Session):
        # Pass Block model to BaseRepository
        super().__init__(session, Block)