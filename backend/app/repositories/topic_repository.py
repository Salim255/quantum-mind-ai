from sqlmodel import select
from sqlalchemy.orm import selectinload
from app.models.topic import Topic
from app.repositories.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.section import Section

class TopicRepository(BaseRepository[Topic]):
    """
    Repository for Topic-specific database queries.

    Inherits common CRUD operations from BaseRepository.
    """

    def __init__(self, session: AsyncSession):
        # Pass Topic model to BaseRepository
        super().__init__(session, Topic)

    async def get_topics_with_sections_with_blocks(self):
        """
        Get a topic along with its sections and blocks.
        """
        statement = select(Topic).options(
            selectinload(Topic.blocks),
            selectinload(Topic.sections).selectinload(Section.blocks)
        )

        # Without scalars(), session.execute() returns Row objects.
        result = await self.session.execute(statement)

        return list(result.scalars().all())