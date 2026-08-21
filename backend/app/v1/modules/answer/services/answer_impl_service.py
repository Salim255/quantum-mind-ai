from fastapi import logger

from app.models.answer import Answer
from app.repositories.answer_repository import AnswerRepository
from app.v1.modules.answer.dto.answer_create_dto import AnswerCreateDTO
from app.v1.modules.answer.dto.answer_dto import AnswerDTO
from app.v1.modules.answer.services.answer_service import AnswerService


class AnswerImplService(AnswerService):
    """
    Concrete implementation of the AnswerService.

    This service contains the business logic required to create
    learning answer options and delegates persistence to the
    AnswerRepository.
    """

    def __init__(
        self,
        answer_repository: AnswerRepository,
    ):
        self.answer_repository = answer_repository

    # ============================================================
    # CREATE
    # ============================================================

    async def create_answer(
        self,
        answer_data: AnswerCreateDTO,
    ) -> AnswerDTO:
        """
        Create and persist a new learning answer.

        The DTO is converted into an Answer entity before being
        passed to the repository.

        Args:
            answer_data:
                Validated data required to create the answer.

        Returns:
            The newly created Answer entity.
        """

        try:
            answer = Answer(
                **answer_data.model_dump()
            )

            await self.answer_repository.add(answer)

            return AnswerDTO.model_validate(answer)

        except Exception:
            logger.exception("Error creating answer")
            raise

