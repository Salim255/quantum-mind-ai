from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.explore.dto.explore_quizzes_response_dto import (
    ExploreQuizzesResponseDTO,
)
from app.v1.modules.explore.dependencies import get_explore_service
from app.v1.modules.explore.services.explore_service import ExploreService

from .router import router as explore_router

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