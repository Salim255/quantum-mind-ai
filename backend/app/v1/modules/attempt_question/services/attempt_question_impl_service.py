from app.models.attempt_question import AttemptQuestion
from app.repositories.attempt_question_repository import (
    AttemptQuestionRepository,
)
from app.v1.modules.attempt_question.dto.attempt_question_create_dto import (
    AttemptQuestionCreateDTO,
)
from app.v1.modules.attempt_question.dto.attempt_question_dto import (
    AttemptQuestionDTO,
)
from app.v1.modules.attempt_question.services.attempt_question_service import (
    AttemptQuestionService,
)
import logging


logger = logging.getLogger(__name__)

class AttemptQuestionImplService(AttemptQuestionService):
    """
    Concrete implementation of the AttemptQuestionService.

    Responsible for applying business rules related to questions
    presented during a quiz attempt and delegating persistence
    to the AttemptQuestionRepository.
    """

    def __init__(
        self,
        attempt_question_repository: AttemptQuestionRepository,
    ):
        self.attempt_question_repository = attempt_question_repository

    async def create_attempt_question(
        self,
        attempt_question_data: AttemptQuestionCreateDTO,
    ) -> AttemptQuestionDTO:
        """
        Create and persist an attempt question.

        The attempt question represents the state of a question
        at the moment it was presented to the user.

        Args:
            attempt_question_data:
                Data required to create the attempt question.

        Returns:
            The persisted attempt question as a DTO.
        """

        try:
            attempt_question = AttemptQuestion(
                attempt_id=attempt_question_data.attempt_id,
                question_id=attempt_question_data.question_id,
                position=attempt_question_data.position,
                question_snapshot=attempt_question_data.question_snapshot,
                question_version=attempt_question_data.question_version,
                difficulty_at_attempt=(
                    attempt_question_data.difficulty_at_attempt
                ),
                concept_id=attempt_question_data.concept_id,
                presented_at=attempt_question_data.presented_at,
                started_at=attempt_question_data.started_at,
                submitted_at=attempt_question_data.submitted_at,
                user_answer=attempt_question_data.user_answer,
                correct_answer=attempt_question_data.correct_answer,
                is_correct=attempt_question_data.is_correct,
                score=attempt_question_data.score,
                time_spent_ms=attempt_question_data.time_spent_ms,
                hint_used=attempt_question_data.hint_used,
                hint_opened_at=attempt_question_data.hint_opened_at,
                explanation_viewed=(
                    attempt_question_data.explanation_viewed
                ),
                confidence=attempt_question_data.confidence,
                attempt_number_for_question=(
                    attempt_question_data.attempt_number_for_question
                ),
                selection_reason=attempt_question_data.selection_reason,
                selection_score=attempt_question_data.selection_score,
            )
            
            await self.attempt_question_repository.add(
                        attempt_question
                    )
            
            return AttemptQuestionDTO.model_validate(
                        attempt_question
                    )
        except Exception:
          logger.exception("Error in create create_attempt_question")
          raise