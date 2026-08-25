from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AttemptQuestionCreateDTO(BaseModel):
    """
    DTO used when creating a question inside a quiz attempt.

    This represents the state of the question when it is selected
    and presented to the user.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    attempt_id: UUID
    """
    The quiz attempt this question belongs to.
    """

    question_id: UUID
    """
    The original question being presented.
    """

    # ============================================================
    # QUIZ POSITION
    # ============================================================

    position: int = Field(
        ge=1,
    )
    """
    Position of the question inside the quiz.

    Example:
        1, 2, 3 ... 15
    """

    # ============================================================
    # QUESTION SNAPSHOT
    # ============================================================

    question_snapshot: dict | None = None
    """
    Optional snapshot of the question content shown to the user.

    Useful when the original question may change later.
    """

    question_version: int | None = None
    """
    Version of the question presented to the user.
    """

    difficulty_at_attempt: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    """
    Difficulty of the question at the time of the attempt.
    """

    concept_id: UUID | None = None
    """
    Optional concept tested by the question.
    """

    # ============================================================
    # TIMING
    # ============================================================

    presented_at: datetime | None = None
    """
    Timestamp when the question was presented.
    """

    started_at: datetime | None = None
    """
    Timestamp when the user started answering.
    """

    # ============================================================
    # SELECTION
    # ============================================================

    selection_reason: str | None = None
    """
    Reason why the question-selection algorithm selected
    this question.
    """

    selection_score: float | None = None
    """
    Priority score calculated when the question was selected.
    """