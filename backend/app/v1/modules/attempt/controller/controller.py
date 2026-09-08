from typing import Annotated
from uuid import UUID
from fastapi import Depends, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container


from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.attempt.dependencies import get_attempt_service
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.attempt.dto.attempt_response_dto import AttemptResponseDTO
from app.v1.modules.attempt.dto.attempt_update_score_dto import AttemptUpdateScoreDTO
from .router import router as attempt_router




# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieve the application dependency container.

    The container owns application-wide dependencies such as:
    - database session management
    - repositories
    - external service clients
    - shared infrastructure services

    Args:
        request:
            Current FastAPI request.

    Returns:
        The application's dependency container.
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
    Provide an asynchronous database session.

    The session is created by the application's database session
    manager and injected into repositories.

    Important:
        This dependency yields the actual AsyncSession.
        It does not expose the DB session manager itself.

    Args:
        container:
            Application dependency container.

    Yields:
        An active asynchronous database session.
    """
    async for session in container.db_session.get_session():
        yield session



# ============================================================
# RETAKE ATTEMPT
# ============================================================

@attempt_router.patch(
    "/{attempt_id}/retake",
    response_model=ResponseDTO[AttemptResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Retake learning attempt",
    description="""
Reset an existing learning attempt for a new quiz session.

The existing attempt is preserved, including its ID, while
its result is reset and a new random set of questions is
assigned to the attempt.

The attempt ID identifies the learning attempt to retake.

The business logic is delegated to AttemptService.
""",
    response_description="The reset learning attempt with its new questions.",
)
async def retake_attempt(
    attempt_id: UUID,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AttemptResponseDTO]:
    """
    Retake an existing learning attempt.

    The controller is intentionally kept thin.
    The AttemptService handles:

    - retrieving the existing attempt
    - resetting the attempt result
    - generating new random questions
    - replacing the attempt questions
    - persisting the changes

    Args:
        attempt_id:
            Identifier of the attempt to retake.

        session:
            Active asynchronous database session.

        container:
            Application dependency container.

    Returns:
        The reset learning attempt with its new questions.
    """

    attempt_service: AttemptService = get_attempt_service(
        session=session,
        container=container,
    )

    attempt = await attempt_service.retake_attempt(
        attempt_id=attempt_id,
    )

    return ResponseDTO.success(attempt)

# ============================================================
# CREATE ATTEMPT
# ============================================================

@attempt_router.post(
    "/",
    response_model=ResponseDTO[AttemptResponseDTO],
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
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ]
) -> ResponseDTO[AttemptResponseDTO]:
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

    attempt_service: AttemptService = get_attempt_service(session=session, container=container)
        
    attempt = await attempt_service.create_attempt(
        payload,
    )

    return ResponseDTO.success(attempt)



# ============================================================
# UPDATE ATTEMPT SCORE
# ============================================================

@attempt_router.patch(
    "/{attempt_id}/score",
    response_model=ResponseDTO[AttemptResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Update attempt score",
    description="""
Evaluate a submitted answer and update the corresponding
learning attempt score.

The attempt ID identifies the attempt being evaluated,
while the answer ID identifies the answer selected by
the learner.

The business logic is delegated to AttemptService.
""",
    response_description="The updated learning attempt.",
)
async def update_score(
    payload: AttemptUpdateScoreDTO,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AttemptResponseDTO]:
    """
    Evaluate the submitted answer and update the attempt score.

    The controller is intentionally kept thin.
    Validation, answer evaluation, score calculation,
    and persistence are handled by AttemptService.

    Args:
        payload:
            Attempt ID and selected answer ID.

        session:
            Active asynchronous database session.

        container:
            Application dependency container.

    Returns:
        The updated learning attempt.
    """

    attempt_service: AttemptService = get_attempt_service(
        session=session,
        container=container,
    )

    attempt = await attempt_service.update_score(
        **payload.model_dump()
    )

    return ResponseDTO.success(attempt)


# ============================================================
# FINISH ATTEMPT
# ============================================================

@attempt_router.patch(
    "/{attempt_id}/finish",
    response_model=ResponseDTO[AttemptResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Finish attempt",
    description="""
Complete a learning attempt.

The attempt ID identifies the learning attempt to complete.

The business logic is delegated to AttemptService.
""",
    response_description="The completed learning attempt.",
)
async def finish_attempt(
    attempt_id: UUID,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AttemptResponseDTO]:
    """
    Complete the specified learning attempt.

    The controller is intentionally kept thin.
    Validation, completion state updates, and persistence
    are handled by AttemptService.

    Args:
        attempt_id:
            Identifier of the attempt to complete.

        session:
            Active asynchronous database session.

        container:
            Application dependency container.

    Returns:
        The completed learning attempt.
    """

    attempt_service: AttemptService = get_attempt_service(
        session=session,
        container=container,
    )

    attempt = await attempt_service.finish_attempt(
        attempt_id=attempt_id,
    )

    return ResponseDTO.success(attempt)