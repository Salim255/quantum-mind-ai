
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict
from app.v1.modules.section.dto.section_with_blocks_dto import SectionWithBlocksDTO


class TopicWithSectionsDTO(BaseModel):
    """
    Data Transfer Object for a Topic along with its Sections.
    Inherits from TopicDTO and adds a list of SectionDTOs.
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

    sections: list[SectionWithBlocksDTO] = []