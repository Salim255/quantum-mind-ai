from pydantic import PostgresDsn
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
import logging

logger = logging.getLogger(__name__)


class DBEngineService:
    """
    Responsible for creating and exposing the async database engine.

    The engine is the main connection manager between the application
    and PostgreSQL.

    Flow:

    FastAPI
        ↓
    Repository
        ↓
    AsyncSession
        ↓
    AsyncEngine
        ↓
    PostgreSQL
    """

    def __init__(self, db_url: PostgresDsn):

        self.db_url = db_url

        self.engine = self.create_engine()


    def create_engine(self) -> AsyncEngine:
        """
        Create an asynchronous SQLAlchemy engine.

        AsyncEngine is required when using AsyncSession.

        Returns:
            AsyncEngine: configured async database engine.
        """

        try:

            engine = create_async_engine(
                str(self.db_url),
                echo=False,
                pool_pre_ping=True,
            )

            logger.info(
                "Async database engine created successfully ✅"
            )

            return engine


        except Exception as e:

            logger.exception(e)

            raise e


    def get_engine(self) -> AsyncEngine:
        """
        Return the application's async engine instance.
        """

        return self.engine