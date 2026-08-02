from typing import Annotated
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container
from app.repositories import topic_repository
from app.repositories.block_repository import BlockRepository
from app.v1.modules.block.service.block_impl_service import BlockImplService
from app.v1.modules.block.service.block_service import BlockService


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

def get_block_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session)
    ],
) -> BlockRepository:
    """
    Creates the block repository.

    Repository responsibility:
        - communicate with database
        - execute queries
        - persist entities
    """

    return BlockRepository(session)



# ============================================================
# SERVICE DEPENDENCY
# ============================================================

def get_block_service(
    block_repository: Annotated[
        BlockRepository,
        Depends(get_block_repository)
    ],
) -> BlockService:
    """
    Creates the block service.

    Service responsibility:
        - business logic
        - validation rules
        - DTO conversion
    """

    return BlockImplService(block_repository)