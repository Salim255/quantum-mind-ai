from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AttemptQuestionDTO(BaseModel):
    """
    DTO returned when reading a question belonging to a quiz attempt.

    Represents the complete state of the question during that
    particular attempt.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    attempt_id: UUID

    question_id: UUID

    # ============================================================
    # QUIZ POSITION
    # ============================================================

    position: int

    # ============================================================
    # QUESTION SNAPSHOT
    # ============================================================

    question_snapshot: dict | None = None

    question_version: int | None = None

    difficulty_at_attempt: int | None = None

    concept_id: UUID | None = None

    # ============================================================
    # TIMING
    # ============================================================

    presented_at: datetime | None = None

    started_at: datetime | None = None

    submitted_at: datetime | None = None

    time_spent_ms: int | None = None

    # ============================================================
    # ANSWER
    # ============================================================

    user_answer: dict | None = None

    correct_answer: dict | None = None

    is_correct: bool | None = None

    score: float | None = None

    # ============================================================
    # ASSISTANCE
    # ============================================================

    hint_used: bool = False

    hint_opened_at: datetime | None = None

    explanation_viewed: bool = False

    # ============================================================
    # CONFIDENCE
    # ============================================================

    confidence: int | None = None

    # ============================================================
    # QUESTION ATTEMPTS
    # ============================================================

    attempt_number_for_question: int = 1

    # ============================================================
    # SELECTION
    # ============================================================

    selection_reason: str | None = None

    selection_score: float | None = None

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime