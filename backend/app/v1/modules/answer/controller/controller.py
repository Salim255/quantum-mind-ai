from typing import Annotated

from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.answer.dependencies import get_answer_service
from app.v1.modules.answer.dto.answer_create_dto import AnswerCreateDTO
from app.v1.modules.answer.dto.answer_dto import AnswerDTO
from app.v1.modules.answer.services.answer_service import AnswerService

from .router import router as answer_router


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
    answer_service: Annotated[
        AnswerService,
        Depends(get_answer_service),
    ],
) -> ResponseDTO[AnswerDTO]:
    """
    Create a new answer option for a learning question.

    The service is responsible for validating the business rules
    and persisting the answer.

    Returns:
        The newly created answer.
    """
    answer = await answer_service.create_answer(payload)

    return ResponseDTO.success(
        AnswerDTO.model_validate(answer)
    )