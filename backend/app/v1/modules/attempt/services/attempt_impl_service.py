import logging
from uuid import UUID
from app.models.attempt import Attempt
from app.repositories.attempt_repository import AttemptRepository
from app.v1.modules.attempt.dto.attempt_create_dto import AttemptCreateDTO
from app.v1.modules.attempt.services.attempt_service import AttemptService
from app.v1.modules.question.services.question_service import QuestionService
from app.v1.modules.answer.services.answer_service import AnswerService
from app.v1.modules.answer.dto.answer_dto import AnswerDTO
from app.v1.modules.attempt_question.services.attempt_question_service import AttemptQuestionService
from app.v1.modules.attempt.dto.attempt_dto import AttemptDTO
from app.v1.modules.topic.dto.topic_dto import TopicDTO
from app.v1.modules.attempt.dto.attempt_response_dto import AttemptResponseDTO
from app.v1.modules.attempt.dto.attempt_update_score_dto import AttemptUpdateScoreResponseDTO


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
        answer_service: AnswerService,
    ):
        self.attempt_repository = attempt_repository
        self.question_service = question_service
        self.answer_service = answer_service
        self.attempt_question_service =  attempt_question_service




    # ============================================================
    # RETAKE ATTEMPT
    # ============================================================

    async def retake_attempt(
        self,
        attempt_id: UUID,
    ) -> AttemptResponseDTO:
        """
        Retake an existing learning attempt.

        Unlike create_attempt(), this operation does not create
        a new Attempt entity.

        The existing attempt is reset and a new random set of
        questions is assigned to it.

        The attempt result is reset:

        - score -> 0
        - correct_answers -> 0
        - is_completed -> False

        The existing attempt ID is preserved.

        Args:
            attempt_id:
                Identifier of the existing learning attempt.

        Returns:
            The reset learning attempt with its new questions.
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
            # 5. PERSIST RESET ATTEMPT
            # ========================================================

            await self.attempt_repository.reset_attempt(
                attempt_id
            )


            # ========================================================
            # 2. LOAD NEW RANDOM QUESTIONS
            # ========================================================

            questions = await self.question_service.get_random_questions_by_topic(
                topic_id=attempt.topic_id,
                limit=attempt.total_questions,
            )


            # ========================================================
            # 6. LOAD ATTEMPT WITH TOPIC
            # ========================================================

            attempt = await self.attempt_repository.get_by_id_with_topic(
                attempt.id
            )

            # ========================================================
            # 7. BUILD TOPIC DTO
            # ========================================================

            topic_dto = TopicDTO.model_validate({
                **attempt.topic.model_dump(),
                "questions": questions,
            })


            # ========================================================
            # 8. BUILD ATTEMPT DTO
            # ========================================================

            attempt_dto = AttemptDTO.model_validate({
                **attempt.model_dump(),
                "topic": topic_dto,
            })


            # ========================================================
            # 9. RETURN SAME RESPONSE SHAPE AS CREATE
            # ========================================================

            return AttemptResponseDTO(
                attempt=attempt_dto
            )

        except Exception:
            logger.exception(
                "Error retaking attempt"
            )
            raise

    # ============================================================
    # FINISH ATTEMPT
    # ============================================================

    async def finish_attempt(
        self,
        attempt_id: UUID,
    ) -> AttemptUpdateScoreResponseDTO:
        """
        Complete a learning attempt.

        The attempt identifies the assessment session.

        The service is responsible for:

        - loading the attempt
        - validating that the attempt exists
        - marking the attempt as completed
        - persisting the updated attempt
        - returning the updated attempt result

        Args:
            attempt_id:
                Identifier of the learning attempt to complete.

        Returns:
            The completed attempt result.
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
            # 2. MARK ATTEMPT AS COMPLETED
            # ========================================================

            attempt.is_completed = True


            # ========================================================
            # 3. PERSIST UPDATED ATTEMPT
            # ========================================================

            await self.attempt_repository.update(
                attempt
            )


            # ========================================================
            # 4. RETURN UPDATED ATTEMPT
            # ========================================================

            attempt_dto = AttemptUpdateScoreResponseDTO(
                id=attempt.id,
                user_id=attempt.user_id,
                topic_id=attempt.topic_id,
                score=attempt.score,
                total_questions=attempt.total_questions,
                correct_answers=attempt.correct_answers,
                is_completed=attempt.is_completed,
            )

            return AttemptResponseDTO(attempt=attempt_dto)
        
        except Exception:
            logger.exception(
                "Error finishing attempt"
            )
            raise

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

            await self.attempt_repository.add_attempt(attempt)


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

            answer: AnswerDTO = await self.answer_service.get_by_id(
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
            # =======================================================

            attempt_dto = AttemptUpdateScoreResponseDTO(
                    id=attempt.id,
                    user_id=attempt.user_id,
                    topic_id=attempt.topic_id,
                    score=attempt.score,
                    total_questions=attempt.total_questions,
                    correct_answers=attempt.correct_answers,
                    is_completed=attempt.is_completed,
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