from uuid import UUID
from pydantic import BaseModel, Field, model_validator


class BlockCreateDTO(BaseModel):
    """
    Payload used to create a learning block.

    A block must belong to either:
    - a Topic (topic introduction), or
    - a Section (section content).

    Exactly one parent must be provided.
    """

    title: str | None = Field(
        default=None,
        max_length=255,
        description="Optional title displayed above the block."
    )

    type: str = Field(
        description="Block type (paragraph, heading, equation, image, exercise, etc.)."
    )

    display_order: int = Field(
            default=0,
            ge=0,
            description="Display order of the block within its parent."
        )   
    
    content: str = Field(
        min_length=1,
        description="Educational content stored inside the block."
    )

    topic_id: UUID | None = Field(
        default=None,
        description="Parent topic identifier."
    )

    section_id: UUID | None = Field(
        default=None,
        description="Parent section identifier."
    )
