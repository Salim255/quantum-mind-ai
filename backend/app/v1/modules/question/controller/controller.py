from typing import Annotated
from app.core.container import Container
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import Depends, status, Request
from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.question.dependencies import get_question_service
from app.v1.modules.question.dto.question_create_dto import QuestionCreateDTO
from app.v1.modules.question.dto.question_dto import QuestionDTO
from app.v1.modules.question.services.question_service import QuestionService

from .router import router as question_router



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
# REPOSITORY DEPENDENCY
# ============================================================


@question_router.post(
    "/",
    response_model=ResponseDTO[QuestionDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a learning question",
    description="""
    Create a new question for a learning topic.

    A question represents a knowledge-check item that can be used
    inside quizzes and practice sessions.

    Each question belongs to exactly one Topic and can contain
    multiple answer options.

    The question can define:

    - question text
    - difficulty level
    - explanation shown after answering
    - content source
    - active/inactive state

    Answer options are managed separately and reference the created
    question through `question_id`.

    The created question is returned after it has been successfully
    persisted.
    """,
    response_description="The newly created learning question.",
)
async def create_question(
    payload: QuestionCreateDTO,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ]
) -> ResponseDTO[QuestionDTO]:
    """
    Create a new learning question.

    This endpoint is typically used by the content-management
    interface when creating or importing educational questions.

    Business rules such as topic validation, difficulty validation,
    and question persistence are handled by the service layer.

    Returns:
        The newly created question.
    """

    question_service: QuestionService = get_question_service(
        session=session
    )

    return ResponseDTO.success(
        await question_service.create_question(payload)
    )