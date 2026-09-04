from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.v1.modules.topic.dto.topic_dto import TopicDTO


class AttemptDTO(BaseModel):
    """
    Represents a user's learning attempt.

    An attempt belongs to one user and one topic.

    When returned for a learning session, the attempt can include
    the questions associated with the topic. Each question can
    contain its available answer options.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID

    # ============================================================
    # OWNERSHIP
    # ============================================================

    user_id: UUID | None = None

    # ============================================================
    # TOPIC
    # ============================================================

    topic_id: UUID

    topic: TopicDTO | None = None


    # ============================================================
    # RESULT
    # ============================================================

    score: float

    total_questions: int

    correct_answers: int

    # ============================================================
    # STATUS
    # ============================================================

    is_completed: bool

    # ============================================================
    # LIFECYCLE
    # ============================================================

    started_at: datetime

    completed_at: datetime | None = None