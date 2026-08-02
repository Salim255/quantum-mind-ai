from sqlmodel import SQLModel
import app.models

from sqlalchemy.ext.asyncio import AsyncEngine

import logging

logger = logging.getLogger(__name__)


class DBInitService:
    """
    Responsible for database schema initialization.

    During early development this service creates tables
    directly from SQLModel metadata.

    In production:
        - Use Alembic migrations.
        - Do not rely on create_all().

    Async Architecture:

        FastAPI Startup
              |
              v
        DBInitService
              |
              v
        AsyncEngine
              |
              v
        run_sync()
              |
              v
        SQLModel.metadata.create_all()
    """


    def __init__(self, engine: AsyncEngine):
        """
        Store the async database engine.

        Args:
            engine:
                SQLAlchemy AsyncEngine used to communicate
                with PostgreSQL.
        """

        self.engine = engine


    async def create_tables(self) -> None:
        """
        Create all registered SQLModel tables.

        SQLModel metadata creation is synchronous internally,
        therefore AsyncEngine.run_sync() is used to safely
        execute create_all().

        Suitable for:
            - Local development
            - Testing environments

        Not recommended for:
            - Production deployments

        Production:
            Use Alembic migrations.
        """

        try:

            logger.info(
                "Registered tables: %s",
                SQLModel.metadata.tables.keys(),
            )


            async with self.engine.begin() as connection:

                await connection.run_sync(
                    SQLModel.metadata.create_all
                )


            logger.info(
                "Database tables initialized successfully ✅"
            )


        except Exception:

            logger.exception(
                "Failed to initialize database tables."
            )

            raise