from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.v1.modules.section.dto.section_with_blocks_dto import SectionWithBlocksDTO
from app.v1.modules.block.dto.block_dto import BlockDTO

class TopicWithSectionsDTO(BaseModel):
    """
    Data Transfer Object for a Topic with nested Sections and Blocks.
    Used when loading a topic together with its learning structure.
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

    display_order: int | None = None
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

    # ==========================================================
    # RELATIONS
    # ==========================================================

    blocks: list[BlockDTO] = Field(default_factory=list)
    
    sections: list[SectionWithBlocksDTO] = Field(default_factory=list)
    """
    Sections belonging to this topic.
    Each section contains its learning blocks.
    """