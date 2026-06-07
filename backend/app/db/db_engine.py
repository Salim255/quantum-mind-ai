from pydantic import PostgresDsn
from sqlmodel import create_engine
from sqlalchemy.engine import Engine
import logging

logger = logging.getLogger(__name__)

class DBEngineService:
    """
    Responsible for creating and exposing the application's
    database engine.

    The engine is SQLAlchemy's central entry point for all
    database communication. Sessions, queries, and transactions
    ultimately use this engine to talk to PostgreSQL.

    Application flow:

    FastAPI
        ↓
    Repositories / Services
        ↓
    SQLModel Sessions
        ↓
    Database Engine (this class)
        ↓
    PostgreSQL
    """

    def __init__(self, db_url: PostgresDsn):
        """
        Initialize the database engine service.

        Args:
            db_url:
                PostgreSQL connection string used to establish
                connections to the database.
        """
        self.db_url = db_url

        # Create the engine once when the application starts.
        # The same engine instance is reused throughout the
        # application's lifetime.
        self.engine = self.create_engine()

    def create_engine(self) -> Engine:
        """
        Create and return a SQLAlchemy engine.

        The engine manages:
        - Database connections
        - Connection pooling
        - SQL execution
        - Transaction communication

        Returns:
            Engine: Configured SQLAlchemy engine instance.
        """

        logger.info("Database engine created successfully..✅✅")

        return create_engine(str(self.db_url))

    def get_engine(self) -> Engine:
        """
        Return the application's engine instance.

        This is typically used when creating database sessions.

        Returns:
            Engine: Active SQLAlchemy engine.
        """
        return self.engine