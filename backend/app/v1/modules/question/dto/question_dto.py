from enum import Enum
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.v1.modules.question.dto.answer_dto import AnswerDTO

# ============================================================
# ENUMS
# ============================================================

class QuestionDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionSource(str, Enum):
    MANUAL = "manual"
    AI = "ai"
    IMPORTED = "imported"





class QuestionDTO(BaseModel):
    """
    Represents a learning question.

    A question belongs to exactly one Topic and may optionally
    include its answer options.

    Answer options are included when the caller requests the
    question together with its answers, for example when building
    a quiz or practice session.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    topic_id: UUID

    question_text: str

    difficulty: QuestionDifficulty

    explanation: str | None = None

    source: QuestionSource

    is_active: bool

    answers: list[AnswerDTO] | None = None

    created_at: datetime

    updated_at: datetime