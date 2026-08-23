from uuid import UUID

from pydantic import BaseModel, Field


class AnswerCreateDTO(BaseModel):
    """
    Payload used to create an answer option for a learning question.

    An answer belongs to exactly one Question and one Topic.

    The topic and question identifiers establish the learning context,
    while the remaining fields define how the answer is presented and
    evaluated.
    """

    # ============================================================
    # LEARNING CONTEXT
    # ============================================================


    question_id: UUID = Field(
        description="Identifier of the Question this answer belongs to."
    )

    # ============================================================
    # CONTENT
    # ============================================================

    text: str = Field(
        min_length=1,
        max_length=1000,
        description="Text displayed as an answer option."
    )

    explanation: str | None = Field(
        default=None,
        max_length=2000,
        description=(
            "Optional explanation shown to the learner after "
            "answer evaluation."
        ),
    )

    # ============================================================
    # ASSESSMENT
    # ============================================================

    is_correct: bool = Field(
        default=False,
        description="Whether this answer is considered correct."
    )

    # ============================================================
    # PRESENTATION
    # ============================================================

    display_order: int = Field(
        default=0,
        ge=0,
        description="Display order of the answer within the question."
    )

