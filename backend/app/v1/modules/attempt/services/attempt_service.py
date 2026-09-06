from abc import ABC, abstractmethod
from uuid import UUID
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO
from app.v1.modules.attempt.dto.attempt_response_dto import AttemptResponseDTO


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
    ) -> AttemptResponseDTO:
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
    async def get_latest_attempt_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID
    ) -> list[AttemptDTO] | None:
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

    # ============================================================
    # UPDATE ATTEMPT SCORE
    # ============================================================

    @abstractmethod
    async def update_score(
        self,
        attempt_id: UUID,
        answer_id: UUID,
    ) -> AttemptResponseDTO:
        """
        Evaluate a submitted answer and update the attempt score.

        The implementation is responsible for:

        - retrieving the attempt
        - retrieving the submitted answer
        - validating that the answer belongs to the attempt
        - determining whether the answer is correct
        - updating the number of correct answers
        - recalculating the attempt score
        - persisting the updated attempt

        Args:
            attempt_id:
                Identifier of the learning attempt being updated.

            answer_id:
                Identifier of the answer submitted by the learner.

        Returns:
            The updated learning attempt.
        """

        raise NotImplementedError(
            "update_score() must be implemented"
        )