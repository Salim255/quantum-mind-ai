from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class DBSessionService:
    """
    Provides asynchronous database sessions.

    Uses SQLAlchemy AsyncSession to allow non-blocking
    database operations inside FastAPI async endpoints.
    """

    def __init__(
        self,
        engine: AsyncEngine,
    ):
        self.engine = engine


    async def get_session(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Creates and provides a database session.

        The session is automatically closed after
        the request finishes.
        """

        async with AsyncSession(
            bind=self.engine
        ) as session:

            yield session