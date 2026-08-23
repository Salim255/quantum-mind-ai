from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AnswerDTO(BaseModel):
    """
    Represents a possible answer option belonging to a learning question.

    An answer belongs to both a Question and a Topic and contains
    the information required to present, order, activate, and
    evaluate the option.
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID

    question_id: UUID

    # ============================================================
    # CONTENT
    # ============================================================

    text: str

    explanation: str | None = None

    # ============================================================
    # ASSESSMENT
    # ============================================================

    is_correct: bool

    # ============================================================
    # PRESENTATION
    # ============================================================

    display_order: int

    # ============================================================
    # STATUS
    # ============================================================

    is_active: bool

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime

    updated_at: datetime