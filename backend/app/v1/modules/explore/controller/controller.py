from typing import Annotated

from fastapi import Depends, status

from collections.abc import AsyncGenerator
from fastapi import Depends, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.explore.dto.explore_quizzes_response_dto import (
    ExploreQuizzesResponseDTO,
)
from app.v1.modules.explore.dependencies import get_explore_service
from app.v1.modules.explore.services.explore_service import ExploreService

from .router import router as explore_router



# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container is stored on FastAPI's application state.

    It provides access to application-wide infrastructure such as:

    - application settings
    - database session management
    - shared infrastructure services

    The controller is responsible for obtaining the container
    because it represents the outer application boundary.
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
) -> AsyncGenerator[
    AsyncSession,
    None,
]:
    """
    Provides the database session for the current request.

    The session is created by the database session manager
    owned by the application container.

    IMPORTANT:

    The controller is the boundary where the database session
    enters the application service layer.

    The session is then explicitly passed to the service factory.

    This allows multiple services and repositories to share
    the exact same AsyncSession.
    """

    async for session in container.db_session.get_session():
        yield session


# ==========================================================
# LIST EXPLORE QUIZZES
# ==========================================================

@explore_router.get(
    "/quizzes",
    response_model=ResponseDTO[ExploreQuizzesResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="List quizzes for exploration",
    description="""
Returns all available quizzes for the Explore page.

Each quiz is represented by:

- The topic associated with the quiz.
- The authenticated user's latest attempt for that topic, if one exists.

If the user has never attempted a topic, `latest_attempt` is `null`.

The endpoint is read-only and does not create or modify attempts.

Used for:

- Explore page
- Quiz catalogue
- Starting a new quiz
- Resuming an unfinished quiz
- Retaking a completed quiz
""",
    response_description="The quizzes available for exploration.",
)
async def get_explore_quizzes(
    explore_service: Annotated[
        ExploreService,
        Depends(get_explore_service),
    ],
) -> ResponseDTO[ExploreQuizzesResponseDTO]:

    return ResponseDTO.success(
        await explore_service.get_quizzes()
    )