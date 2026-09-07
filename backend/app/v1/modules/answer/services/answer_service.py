from abc import ABC, abstractmethod
from uuid import UUID
from app.v1.modules.answer.dto.answer_create_dto import AnswerCreateDTO
from app.v1.modules.answer.dto.answer_dto import AnswerDTO


class AnswerService(ABC):
    """
    Defines the business operations available for learning answers.

    The service layer is responsible for business rules and orchestration.
    Database access is delegated to the AnswerRepository.
    """

    @abstractmethod
    async def create_answer(
        self,
        answer_data: AnswerCreateDTO,
    )-> AnswerDTO:
        """
        Create a new answer option.

        The implementation is responsible for validating the
        business context and persisting the answer.

        Args:
            answer_data:
                Data required to create the answer.

        Returns:
            The created Answer entity.
        """
        raise NotImplementedError(
            "create_answer() must be implemented"
        )


    # ============================================================
    # GET ANSWER BY ID
    # ============================================================

    @abstractmethod
    async def get_by_id(
        self,
        answer_id: UUID,
    ) -> AnswerDTO | None:
        """
        Retrieve an answer by its identifier.

        Args:
            answer_id:
                Identifier of the answer to retrieve.

        Returns:
            The matching Answer entity if it exists,
            otherwise None.
        """

        raise NotImplementedError(
            "get_by_id() must be implemented"
        )