from sqlmodel import SQLModel
import logging

logger = logging.getLogger(__name__)

class DBInitService:
    def __init__(self, engine):
        self.engine = engine
    def create_tables(self):
        # Tables should be created with Alembic migrations
        # But if you don't want to use migrations, create
        # the tables un-commenting the next lines
        # from sqlmodel import SQLModel

        # This works because the models are already imported and registered from app.models
        # SQLModel.metadata.create_all(engine)
        try:
            SQLModel.metadata.create_all(self.engine)
        except Exception as e:
            logger.exception(e)
            raise e