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

        try:

            # ------------------------------------------------------
            # Get ALL topics.
            #
            # Topics are always returned, regardless of whether
            # the user has attempted them.
            # ------------------------------------------------------

            topics_response = await self.topic_service.get_topics()


            quizzes = []


            # ------------------------------------------------------
            # Go through EVERY topic.
            # ------------------------------------------------------

            for topic in topics_response.topics:

                latest_attempt = None


                # --------------------------------------------------
                # If there is an authenticated user, try to find
                # THEIR latest attempt for THIS specific topic.
                # --------------------------------------------------

                if user_id is not None:

                    latest_attempt = (
                        await self.attempt_service
                        .get_latest_attempt_by_user_and_topic(
                            user_id=user_id,
                            topic_id=topic.id,
                        )
                    )


                # --------------------------------------------------
                # Always add the topic.
                #
                # If the user has no attempt:
                #
                #     latest_attempt = None
                #
                # The topic is still returned.
                # --------------------------------------------------

                quizzes.append(
                    ExploreQuizDTO(
                        topic=topic,
                        latest_attempt=latest_attempt,
                    )
                )


            # ------------------------------------------------------
            # Return ALL topics with their corresponding latest
            # user attempt.
            # ------------------------------------------------------

            return ExploreQuizzesResponseDTO(
                quizzes=quizzes,
            )


        except Exception as e:

            logger.exception(
                "Error retrieving Explore quizzes: %s",
                e,
            )

            raise