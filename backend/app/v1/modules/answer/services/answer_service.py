from abc import ABC, abstractmethod

from app.v1.modules.answer.dto.answer_create_dto import AnswerCreateDTO


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
    ):
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

