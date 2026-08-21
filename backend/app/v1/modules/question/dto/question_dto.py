from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.v1.modules.answer.dto.answer_dto import AnswerDTO


# ============================================================
# ENUMS
# ============================================================


class QuestionDifficulty(str, Enum):
    """
    Defines the difficulty level of a learning question.
    """

    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionSource(str, Enum):
    """
    Defines how the question was created or imported.
    """

    MANUAL = "manual"
    AI = "ai"
    IMPORTED = "imported"


# ============================================================
# DTO
# ============================================================


class QuestionDTO(BaseModel):
    """
    Represents a learning question.

    A question belongs to exactly one Topic and may optionally
    include its answer options.

    Answers are included when the question is loaded together
    with its relationships, for example when building a quiz
    or practice session.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID

    # ============================================================
    # TOPIC
    # ============================================================

    topic_id: UUID

    # ============================================================
    # CONTENT
    # ============================================================

    text: str

    explanation: str | None = None

    # ============================================================
    # ASSESSMENT
    # ============================================================

    difficulty: QuestionDifficulty

    # ============================================================
    # PRESENTATION
    # ============================================================

    display_order: int

    # ============================================================
    # CONTENT SOURCE
    # ============================================================

    source: QuestionSource

    # ============================================================
    # STATUS
    # ============================================================

    is_active: bool

    # ============================================================
    # ANSWERS
    # ============================================================

    answers: list[AnswerDTO] | None = None

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime

    updated_at: datetime