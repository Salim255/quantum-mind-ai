from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container
from app.repositories.topic_repository import TopicRepository
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.topic.service.topic_impl_service import TopicImplService


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request
) -> Container:
    """
    Retrieves the application dependency container.

    The container owns shared services such as:
    - database session service
    - repositories
    - external clients
    """
    return request.app.state.container



# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db_session(
    container: Annotated[
        Container,
        Depends(get_container)
    ],
):
    """
    Provides an async SQLAlchemy database session.

    The repository layer receives this object.

    Important:
        This is NOT DBSessionService.
        This is the actual AsyncSession.
    """

    async for session in container.db_session.get_session():
        yield session



# ============================================================
# REPOSITORY DEPENDENCY
# ============================================================

def get_topic_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session)
    ],
) -> TopicRepository:
    """
    Creates the topic repository.

    Repository responsibility:
        - communicate with database
        - execute queries
        - persist entities
    """

    return TopicRepository(session)



# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_topic_service(
    topic_repository: Annotated[
        TopicRepository,
        Depends(get_topic_repository)
    ],
) -> TopicService:
    """
    Creates the topic service.

    Service responsibility:
        - business logic
        - validation rules
        - DTO conversion
    """

    return TopicImplService(topic_repository)