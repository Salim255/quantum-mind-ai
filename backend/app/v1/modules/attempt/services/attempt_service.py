from abc import ABC, abstractmethod
from uuid import UUID
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


    # ============================================================
    # GET LATEST ATTEMPTS
    # ============================================================

    @abstractmethod
    async def get_latest_attempts_by_topic(
        self,
        user_id: UUID | None,
    ) -> list[AttemptDTO]:
        """
        Retrieves the latest attempt made by the user for each topic.

        This is used by the Explore page to display the current
        state of each quiz.

        For every topic, there can be at most one returned attempt.

        The returned attempt can be:

            - None for topics never attempted by the user
            - incomplete
            - completed

        The service is responsible for determining which attempt
        is the latest for each topic.

        Args:
            user_id:
                Identifier of the current user.

                None can be used for an anonymous user.

        Returns:
            A list containing the latest attempt for each topic.
        """

        raise NotImplementedError(
            "get_latest_attempts_by_topic() must be implemented"
        )