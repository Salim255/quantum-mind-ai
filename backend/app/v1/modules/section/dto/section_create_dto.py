from uuid import UUID

from pydantic import BaseModel, Field


class SectionCreateDTO(BaseModel):
    """
    Data Transfer Object used to create a new learning section.

    A section represents a logical chapter within a learning topic.

    Sections organize educational content into a structured,
    navigable hierarchy. The actual educational content is
    stored separately as Blocks.
    """

    title: str = Field(
        max_length=255,
        description=(
            "Human-readable title of the section.\n\n"
            "Example:\n"
            "'Introduction to Spin'"
        ),
    )

    slug: str = Field(
        max_length=255,
        description=(
            "URL-friendly unique identifier of the section.\n\n"
            "Example:\n"
            "'introduction-to-spin'"
        ),
    )

    description: str | None = Field(
        default=None,
        description=(
            "Optional short summary displayed before entering the section."
        ),
    )

    order_index: int = Field(
        default=0,
        ge=0,
        description=(
            "Display order of the section within its parent topic."
        ),
    )

    topic_id: UUID = Field(
        description=(
            "Identifier of the topic that owns this section."
        ),
    )