from abc import ABC, abstractmethod
from uuid import UUID

from app.v1.modules.explore.dto.explore_quizzes_response_dto import (
    ExploreQuizzesResponseDTO,
)


class ExploreService(ABC):
    """
    Defines the contract for Explore business operations.

    The Explore module is responsible for preparing the data required
    by the Explore page.

    The Explore page combines information coming from multiple modules:

        Topic
          +
        User's latest Attempt
          =
        Explore Quiz

    Responsibilities:

        - Retrieve the quizzes displayed in Explore
        - Combine topic information with the current user's latest attempt
        - Return a presentation-ready Explore response

    The service does not handle:

        - database queries
        - SQL operations
        - HTTP concerns

    Those responsibilities belong to:

        Repository layer
        Controller/API layer
    """

    # ==========================================================
    # GET EXPLORE QUIZZES
    # ==========================================================

    @abstractmethod
    async def get_explore_quizzes(
        self,
        user_id: UUID | None,
    ) -> ExploreQuizzesResponseDTO:
        """
        Retrieves the quizzes displayed on the Explore page.

        For every available topic, the response contains:

            - Topic information
            - The current user's latest attempt, if one exists

        If the user has never attempted a topic:

            latest_attempt = None

        This allows the frontend to determine the appropriate action:

            No attempt
                -> Take Quiz

            Incomplete latest attempt
                -> Resume

            Completed latest attempt
                -> Retake

        Args:
            user_id:
                The current user's identifier.

                Anonymous users can be represented with None.

        Returns:
            ExploreQuizzesResponseDTO
        """

        raise NotImplementedError(
            "get_explore_quizzes() must be implemented"
        )