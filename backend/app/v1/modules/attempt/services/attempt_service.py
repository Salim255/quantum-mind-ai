from abc import ABC, abstractmethod

from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO


class AttemptService(ABC):
    """
    Defines the business operations available for learning attempts.

    The service layer is responsible for attempt-related business
    rules and orchestration.

    Database access is delegated to repositories.
    """

    @abstractmethod
    async def create_attempt(
        self,
        attempt_data: AttemptCreateDTO,
    ) -> AttemptDTO:
        """
        Create a new learning attempt.

        The implementation is responsible for:

        - validating the topic
        - resolving the questions belonging to the topic
        - initializing the attempt result
        - persisting the attempt

        Args:
            attempt_data:
                Data required to create the attempt.

        Returns:
            The created Attempt entity.
        """
        raise NotImplementedError(
            "create_attempt() must be implemented"
        )