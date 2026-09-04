from typing import Annotated
from fastapi import Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container
from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.attempt.dependencies import get_attempt_service
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService

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
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ]
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

    attempt_service: AttemptService = get_attempt_service(session=session, container=container)
        
    attempt = await attempt_service.create_attempt(
        payload,
    )

    return ResponseDTO.success(attempt=attempt)

