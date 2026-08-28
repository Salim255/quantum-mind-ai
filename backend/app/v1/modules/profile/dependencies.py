from typing import Annotated

from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container

from app.repositories.profile_repository import (
    ProfileRepository,
)

from app.v1.modules.profile.services.profile_service import (
    ProfileService,
)

from app.v1.modules.profile.services.profile_impl_service import (
    ProfileImplService,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container provides access to application-wide
    infrastructure and shared dependencies.
    """

    return request.app.state.container


# ============================================================
# DATABASE SESSION DEPENDENCY
# ============================================================

async def get_db_session(
    container: Annotated[
        Container,
        Depends(get_container),
    ],
):
    """
    Provides an asynchronous database session.

    The session is shared across all repositories involved
    in the same request.
    """

    async for session in container.db_session.get_session():
        yield session


# ============================================================
# PROFILE REPOSITORY
# ============================================================

def get_profile_repository(
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
) -> ProfileRepository:
    """
    Creates the profile repository.

    Responsible for persistence operations related to
    user profiles.
    """

    return ProfileRepository(session)


# ============================================================
# PROFILE SERVICE
# ============================================================

def get_profile_service(
    profile_repository: Annotated[
        ProfileRepository,
        Depends(get_profile_repository),
    ],
) -> ProfileService:
    """
    Creates the profile service.

    ProfileService coordinates profile operations while
    delegating persistence responsibilities to
    ProfileRepository.

    Dependencies:

    ProfileRepository
        Provides persistence operations for user profiles.
    """

    return ProfileImplService(
        profile_repository=profile_repository,
    )