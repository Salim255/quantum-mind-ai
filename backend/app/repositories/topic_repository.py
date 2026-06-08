from sqlmodel import Session, select
from models.topic import Topic
from repositories.base_repository import BaseRepository


class TopicRepository(BaseRepository[Topic]):
    """
    Repository for Topic-specific database queries.

    Inherits common CRUD operations from BaseRepository.
    """

    def __init__(self, session: Session):
        # Pass Topic model to BaseRepository
        super().__init__(session, Topic)

    # -----------------------------
    # GET BY SLUG
    # -----------------------------
    def get_by_slug(self, slug: str):
        """
        Find a topic using its unique slug.
        """
        statement = select(Topic).where(Topic.slug == slug)
        return self.session.exec(statement).first()

    # -----------------------------
    # GET BY CATEGORY
    # -----------------------------
    def get_by_category(self, category: str):
        """
        Get all topics in a category.
        """
        statement = select(Topic).where(Topic.category == category)
        return self.session.exec(statement).all()