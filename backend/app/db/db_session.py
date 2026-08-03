from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class DBSessionService:
    """
    Provides asynchronous database sessions.

    Uses SQLAlchemy AsyncSession to allow non-blocking
    database operations inside FastAPI async endpoints.
    """

    def __init__(
        self,
        engine,
    ):
        self.session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )


    async def get_session(
        self,
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Creates and provides a database session.

        The session is automatically closed after
        the request finishes.
        """

        async with self.session_factory() as session:

            yield session