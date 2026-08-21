from uuid import UUID

from pydantic import BaseModel, Field


class AttemptCreateDTO(BaseModel):
    """
    Payload used to create a new learning attempt.

    An attempt is created for one user and one topic.
    The questions belonging to the topic are resolved by the backend.

    Result-related fields such as score, correct answers, completion
    status, and timestamps are managed by the application.
    """

    # ============================================================
    # OWNERSHIP
    # ============================================================

    user_id: UUID = Field(
        description="Identifier of the user starting the attempt.",
    )

    # ============================================================
    # TOPIC
    # ============================================================

    topic_id: UUID = Field(
        description="Identifier of the topic being attempted.",
    )