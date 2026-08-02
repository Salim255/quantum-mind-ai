
from typing import Annotated, Container

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.section_repository import SectionRepository
from app.v1.modules.block.dependencies import get_db_session
from app.v1.modules.section.service.section_service import SectionService
from app.v1.modules.section.service.section_impl_service import SectionImplService

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

    
def get_section_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session)
    ],
) -> SectionRepository:
    """
    Creates the section repository.

    Repository responsibility:
        - database access
        - CRUD operations
        - query building
    """

    return SectionRepository(session)


def get_section_service(
    section_repository: Annotated[
        SectionRepository,
        Depends(get_section_repository)
    ],
) -> SectionService:
    """
    Creates the section service.

    Service responsibility:
        - orchestrate business logic
        - coordinate between repositories
        - handle transactions
    """

    return SectionImplService(section_repository)