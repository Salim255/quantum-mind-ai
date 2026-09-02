from typing import Annotated

from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.attempt.dependencies import get_attempt_service
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService

from .router import router as attempt_router


# ============================================================
# CREATE ATTEMPT
# ============================================================

@attempt_router.post(
    "/",
    response_model=ResponseDTO[AttemptDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a learning attempt",
    description="""
Create a new learning attempt for a topic.

An attempt represents one learner's assessment session
for a specific topic.

The attempt is associated with:

- a user
- a topic
- the questions available for that topic

The initial score and answer counters are initialized when
the attempt is created.

The created attempt is returned after it has been successfully
persisted.
""",
    response_description="The newly created learning attempt.",
)
async def create_attempt(
    payload: AttemptCreateDTO,
    attempt_service: Annotated[
        AttemptService,
        Depends(get_attempt_service),
    ],
) -> ResponseDTO[AttemptDTO]:
    """
    Create a new learning attempt.

    The controller is intentionally kept thin.
    Business rules and persistence are delegated to the
    AttemptService.

    Args:
        payload:
            Data required to create the attempt.

        attempt_service:
            Injected attempt service.

    Returns:
        The newly created learning attempt.
    """
    attempt = await attempt_service.create_attempt(
        payload,
    )

    return ResponseDTO.success(attempt)

