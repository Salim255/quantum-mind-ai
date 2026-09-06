from typing import Annotated

from fastapi import Depends, Request, status
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.container import Container

from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.answer.dependencies import get_answer_service
from app.v1.modules.answer.dto.answer_create_dto import AnswerCreateDTO
from app.v1.modules.answer.dto.answer_dto import AnswerDTO
from app.v1.modules.answer.services.answer_service import AnswerService

from .router import router as answer_router


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
        
@answer_router.post(
    "/",
    response_model=ResponseDTO[AnswerDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Create a learning answer",
    description="""
Create a new answer option for a learning question.

An answer belongs to:

- a Question
- a Topic

The answer can be marked as correct or incorrect and can
define its display order within the question.

The created answer is returned after it has been successfully
persisted.
""",
    response_description="The newly created learning answer.",
)
async def create_answer(
    payload: AnswerCreateDTO,
    session: Annotated[
        AsyncSession,
        Depends(get_db_session),
    ],
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> ResponseDTO[AnswerDTO]:
    """
    Create a new answer option for a learning question.

    The service is responsible for validating the business rules
    and persisting the answer.

    Returns:
        The newly created answer.
    """


    answer_service: AnswerService = get_answer_service(
        session=session,
        container=container,
    )
    answer = await answer_service.create_answer(payload)

    return ResponseDTO.success(answer)
