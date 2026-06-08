from sqlmodel import SQLModel
from sqlalchemy.engine import Engine
import logging

logger = logging.getLogger(__name__)


class DBInitService:
    """
    Responsible for database schema initialization.

    During early development this service can create tables
    directly from SQLModel metadata.

    In production, schema changes should be managed through
    Alembic migrations instead of create_all().
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def create_tables(self) -> None:
        """
        Create all registered SQLModel tables.

        This method scans SQLModel metadata and creates any
        tables that do not already exist.

        Notes:
            - Suitable for local development.
            - Not recommended for production environments.
            - Production deployments should use Alembic migrations.

        Raises:
            Exception: Re-raises any database initialization errors.
        """
        try:
            SQLModel.metadata.create_all(self.engine)

            logger.info(
                "Database tables initialized successfully. ✅"
            )

        except Exception:
            logger.exception(
                "Failed to initialize database tables."
            )
            raise