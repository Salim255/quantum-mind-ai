from typing import Annotated

from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO
from app.v1.modules.question.dependencies import get_question_service
from app.v1.modules.question.dto.question_create_dto import QuestionCreateDTO
from app.v1.modules.question.dto.question_dto import QuestionDTO
from app.v1.modules.question.services.question_service import QuestionService

from .router import router as question_router


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
    question_service: Annotated[
        QuestionService,
        Depends(get_question_service),
    ],
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
    return ResponseDTO.success(
        await question_service.create_question(payload)
    )