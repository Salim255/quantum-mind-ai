from uuid import UUID

from pydantic import BaseModel, Field

from app.v1.modules.question.dto.question_dto import QuestionDifficulty
from app.v1.modules.question.dto.question_dto import QuestionSource


class QuestionCreateDTO(BaseModel):
    """
    Payload used to create a learning question.

    A question belongs to exactly one Topic and represents a
    reusable knowledge-check item that can be used by quizzes,
    practice sessions, and other learning experiences.

    Answer options are created separately and reference the
    resulting question through `question_id`.
    """

    topic_id: UUID = Field(
        description="Identifier of the topic to which the question belongs."
    )

    text: str = Field(
        min_length=1,
        max_length=2000,
        description="The question presented to the learner."
    )

    difficulty: QuestionDifficulty = Field(
        default=QuestionDifficulty.EASY,
        description="Difficulty level of the question."
    )

    explanation: str | None = Field(
        default=None,
        max_length=5000,
        description=(
            "Optional explanation presented to the learner after "
            "answering the question."
        ),
    )

    source: QuestionSource = Field(
        default=QuestionSource.MANUAL,
        description=(
            "Origin of the question, such as manually authored "
            "or generated content."
        ),
    )

    is_active: bool = Field(
        default=True,
        description=(
            "Determines whether the question can be used in "
            "new learning sessions."
        ),
    )