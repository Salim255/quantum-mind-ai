import logging
from uuid import UUID
from app.models.attempt import Attempt
from app.repositories.attempt_repository import AttemptRepository
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.question.services.question_service import QuestionService
from app.v1.modules.answer.services.answer_service import AnswerService
from app.v1.modules.attempt_question.services.attempt_question_service import AttemptQuestionService
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO
from app.v1.modules.attempt.dto.attempt_response_dto import AttemptResponseDTO


logger = logging.getLogger(__name__)

class AttemptImplService(AttemptService):
    """
    Concrete implementation of the AttemptService.

    Responsible for creating and initializing learning attempts.

    The service coordinates the AttemptRepository and
    QuestionRepository because an attempt is created from
    the questions belonging to a specific topic.
    """

    def __init__(
        self,
        attempt_repository: AttemptRepository,
        question_service: QuestionService,
        attempt_question_service: AttemptQuestionService,
        answerService: AnswerService,
    ):
        self.attempt_repository = attempt_repository
        self.question_service = question_service

    # ============================================================
    # CREATE
    # ============================================================

    async def create_attempt(
        self,
        attempt_data: AttemptCreateDTO,
    ) -> AttemptResponseDTO:
        """
        Create and initialize a new learning attempt.

        The questions are resolved from the supplied topic.
        The number of active questions becomes the attempt's
        total_questions value.

        Args:
            attempt_data:
                Validated attempt creation data.

        Returns:
            The newly created Attempt entity.
        """

        try:
            
            # 1 Create attempt

            attempt = Attempt(
                user_id=attempt_data.user_id,
                topic_id=attempt_data.topic_id,
                score=0.0,
                total_questions=15,
                correct_answers=0,
                is_completed=False,
            )

            await self.attempt_repository.add(attempt)


            # ============================================================
            # 2. BUILD ATTEMPT QUESTIONS
            # ============================================================
            questions =  await self.question_service.get_random_questions_by_topic(
                topic_id=attempt_data.topic_id,
                limit=15,
            )

   
            # ============================================================
            # 3. LOAD ATTEMPT WITH TOPIC
            # ============================================================
            attempt = await self.attempt_repository.get_by_id_with_topic(
                attempt.id
            )

            # 4
            topic_dto = TopicDTO.model_validate({
                **attempt.topic.model_dump(),
                "questions": questions,
            })
            

            # 5
            attempt_dto = AttemptDTO.model_validate({
                **attempt.model_dump(),
                "topic": topic_dto,
            })


            # 6
            return AttemptResponseDTO(attempt=attempt_dto)

        except Exception:
            logger.exception("Error creating attempt")
            raise
    
    # ============================================================
    # UPDATE SCORE
    # ============================================================

    async def update_score(
        self,
        attempt_id: UUID,
        answer_id: UUID,
    ) -> AttemptResponseDTO:
        """
        Evaluate a submitted answer and update the attempt score.

        The attempt identifies the assessment session and the
        answer identifies the answer selected by the learner.

        The service is responsible for:

        - loading the attempt
        - loading the submitted answer
        - determining whether the answer is correct
        - updating correct_answers
        - recalculating the score
        - persisting the updated attempt
        - returning the updated attempt
        """

        try:

            # ========================================================
            # 1. LOAD ATTEMPT
            # ========================================================

            attempt = await self.attempt_repository.get_by_id(
                attempt_id
            )

            if not attempt:
                raise ValueError(
                    f"Attempt {attempt_id} not found"
                )


            # ========================================================
            # 2. LOAD ANSWER
            # ========================================================

            answer = await self.answer_service.get_by_id(
                answer_id
            )

            if not answer:
                raise ValueError(
                    f"Answer {answer_id} not found"
                )


            # ========================================================
            # 3. EVALUATE ANSWER
            # ========================================================

            if answer.is_correct:
                attempt.correct_answers += 1


            # ========================================================
            # 4. RECALCULATE SCORE
            # ========================================================

            if attempt.total_questions > 0:

                attempt.score = (
                    attempt.correct_answers
                    / attempt.total_questions
                ) * 100

            else:

                attempt.score = 0.0


            # ========================================================
            # 5. PERSIST UPDATED ATTEMPT
            # ========================================================

            await self.attempt_repository.update(
                attempt
            )


            # ========================================================
            # 6. RETURN UPDATED ATTEMPT
            # ========================================================

            attempt_dto = AttemptDTO.model_validate(
                attempt
            )

            return AttemptResponseDTO(
                attempt=attempt_dto
            )

        except Exception:
            logger.exception(
                "Error updating attempt score"
            )
            raise

    # ============================================================
    # GET LATEST ATTEMPTS BY TOPIC
    # ============================================================

    async def get_latest_attempt_by_user_and_topic(
        self,
        user_id: UUID,
        topic_id: UUID
    ) -> list[AttemptDTO] | None:
        """
        Retrieves the latest attempt for each topic belonging
        to the specified user.

        The repository is responsible for retrieving the
        appropriate attempts from the database.

        The service converts the resulting entities into
        AttemptDTO objects.
        """

        try:

            attempts = (
                await self.attempt_repository
                .get_latest_attempt_by_user_and_topic(
                    user_id=user_id,
                    topic_id=topic_id
                )
            )

            return [
                AttemptDTO.model_validate(attempt)
                for attempt in attempts
            ]

        except Exception:
            logger.exception(
                "Error retrieving latest attempts by topic"
            )
            raise