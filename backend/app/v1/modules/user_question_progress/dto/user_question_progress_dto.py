from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserQuestionProgressDTO(BaseModel):
    """
    Represents the complete learning progress of a user
    for a specific question.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID

    user_id: UUID

    question_id: UUID

    # ============================================================
    # EXPOSURE
    # ============================================================

    first_seen_at: datetime | None = None

    last_seen_at: datetime | None = None

    # ============================================================
    # ATTEMPTS
    # ============================================================

    attempt_count: int

    correct_count: int

    incorrect_count: int

    accuracy: Decimal

    last_result: bool | None = None

    # ============================================================
    # STREAKS
    # ============================================================

    consecutive_correct: int

    consecutive_incorrect: int

    best_streak: int

    # ============================================================
    # TIME
    # ============================================================

    total_time_ms: int

    average_time_ms: int | None = None

    fastest_time_ms: int | None = None

    slowest_time_ms: int | None = None

    # ============================================================
    # ASSISTANCE
    # ============================================================

    hints_used: int

    explanations_viewed: int

    # ============================================================
    # CONFIDENCE
    # ============================================================

    confidence_avg: Decimal | None = None

    # ============================================================
    # MASTERY
    # ============================================================

    mastery_score: Decimal

    mastery_level: int

    # ============================================================
    # DIFFICULTY
    # ============================================================

    difficulty_estimate: Decimal | None = None

    last_difficulty: int | None = None

    # ============================================================
    # SPACED REPETITION
    # ============================================================

    stability_days: Decimal

    retrievability: Decimal

    next_review_at: datetime | None = None

    review_count: int

    overdue: bool

    # ============================================================
    # PRIORITY
    # ============================================================

    weakness_score: Decimal

    priority_score: Decimal

    last_priority_calculated_at: datetime | None = None

    # ============================================================
    # MASTERY LIFECYCLE
    # ============================================================

    mastered_at: datetime | None = None

    # ============================================================
    # AUDIT
    # ============================================================

    updated_at: datetime

    created_at: datetime