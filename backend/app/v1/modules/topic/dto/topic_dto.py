from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.v1.modules.question.dto.question_dto import QuestionDTO


class TopicDTO(BaseModel):
    """
    DTO returned when reading a QuantumMind learning topic.

    A topic is the owner of its learning questions.

    Questions are exposed through the topic rather than duplicated
    on other resources such as AttemptDTO.

    This allows consumers to access:

        topic.questions
            └── question.answers

    The questions relationship is populated only when the underlying
    query loads the Topic.questions relationship.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ==========================================================
    # IDENTITY
    # ==========================================================

    id: UUID
    """
    Unique identifier of the topic.
    """

    title: str
    """
    Human-readable topic title displayed to learners.
    """

    slug: str
    """
    Public URL-friendly identifier of the topic.
    """

    # ==========================================================
    # CLASSIFICATION
    # ==========================================================

    category: str
    """
    Learning category used to organize topics.
    """

    display_order: int | None
    """
    Controls the order of topics within their category.
    """

    # ==========================================================
    # PRESENTATION
    # ==========================================================

    description: str | None = None
    """
    Short introduction displayed before opening the topic.
    """

    # ==========================================================
    # QUESTIONS
    # ==========================================================

    questions: list[QuestionDTO] = []
    """
    Questions belonging to this topic.

    Questions are obtained through the Topic.questions relationship.

    Each QuestionDTO may contain its answer options when those
    answers have been loaded by the repository query.
    """

    # ==========================================================
    # METADATA
    # ==========================================================

    created_at: datetime
    """
    Timestamp when the topic was created.
    """

    updated_at: datetime
    """
    Timestamp when the topic was last modified.
    """