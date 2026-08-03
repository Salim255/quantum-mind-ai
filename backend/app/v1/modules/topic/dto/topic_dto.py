from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TopicDTO(BaseModel):
    """
    DTO returned when reading a QuantumMind learning topic.

    Represents the public topic information exposed by the API.

    This DTO is used for:
    - Created topic responses
    - Topic details pages
    - Topic listings

    Database-only fields are intentionally excluded.
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
    Used internally for database relations.
    """


    title: str
    """
    Human-readable topic title displayed to learners.
    """


    slug: str
    """
    Public URL-friendly identifier of the topic.
    Example:
        quantum-entanglement
    """


    # ==========================================================
    # CLASSIFICATION
    # ==========================================================

    category: str
    """
    Learning category used to organize topics.
    Example:
        Quantum Physics
    """

    display_order: int | None
    """
    Controls the order of topics within a category.
    Lower numbers appear first in listings.
    """

    # ==========================================================
    # PRESENTATION
    # ==========================================================

    description: str
    """
    Short introduction displayed before opening the topic.
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