import logging
from uuid import UUID

from app.v1.modules.explore.dto.explore_quizzes_response_dto import (
    ExploreQuizDTO,
    ExploreQuizzesResponseDTO,
)
from app.v1.modules.explore.services.explore_service import ExploreService
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.attempt.services.attempt_service import AttemptService


logger = logging.getLogger(__name__)


class ExploreImplService(ExploreService):
    """
    Implements the business logic required by the Explore page.

    Explore does not own Topic or Attempt data.

    It composes data from:
        - TopicService
        - AttemptService

    For every topic, we attach the current user's latest attempt,
    when one exists.
    """

    def __init__(
        self,
        topic_service: TopicService,
        attempt_service: AttemptService,
    ):
        self.topic_service = topic_service
        self.attempt_service = attempt_service


    # ==========================================================
    # GET EXPLORE QUIZZES
    # ==========================================================

    async def get_explore_quizzes(
        self,
        user_id: UUID | None,
    ) -> ExploreQuizzesResponseDTO:
        """
        Retrieves the quizzes displayed on the Explore page.

        Each quiz contains:

            topic
            latest_attempt | None

        The latest attempt belongs to the current user.

        The frontend can use the attempt status to determine
        the appropriate action:

            No attempt
                -> Take Quiz

            Incomplete attempt
                -> Resume

            Completed attempt
                -> Retake
        """

        try:

            # ------------------------------------------------------
            # Get all available topics.
            # ------------------------------------------------------

            topics_response = (
                await self.topic_service.get_topics()
            )


            # ------------------------------------------------------
            # Get the current user's latest attempt for each topic.
            #
            # AttemptService owns the logic for retrieving attempts.
            # Explore only consumes the result.
            # ------------------------------------------------------

            latest_attempts = (
                await self.attempt_service
                .get_latest_attempt_by_user_and_topic(
                    user_id=user_id,
                )
            )


            # ------------------------------------------------------
            # Create a lookup by topic ID.
            #
            # This lets us associate an attempt with its topic
            # without repeatedly searching the attempts list.
            # ------------------------------------------------------

            attempts_by_topic = {
                attempt.topic_id: attempt
                for attempt in latest_attempts
            }


            # ------------------------------------------------------
            # Compose the Explore quiz list.
            # ------------------------------------------------------

            quizzes = [

                ExploreQuizDTO(
                    topic=topic,
                    latest_attempt=attempts_by_topic.get(
                        topic.id
                    ),
                )

                for topic in topics_response.topics

            ]


            # ------------------------------------------------------
            # Return the complete Explore response.
            # ------------------------------------------------------

            return ExploreQuizzesResponseDTO(
                quizzes=quizzes,
            )


        except Exception as e:

            logger.exception(f"Error retrieving Explore quizzes: {e}")

            raise