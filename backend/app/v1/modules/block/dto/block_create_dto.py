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

    content: str = Field(
        min_length=1,
        description="Educational content stored inside the block."
    )

    order_index: int = Field(
        default=0,
        ge=0,
        description="Display order inside its parent."
    )

    topic_id: UUID | None = Field(
        default=None,
        description="Parent topic identifier."
    )

    section_id: UUID | None = Field(
        default=None,
        description="Parent section identifier."
    )

    @model_validator(mode="after")
    def validate_parent(self):
        """
        A block must belong to exactly one parent.
        """
        if (self.topic_id is None) == (self.section_id is None):
            raise ValueError(
                "A block must belong to either a topic or a section (but not both)."
            )
        return self