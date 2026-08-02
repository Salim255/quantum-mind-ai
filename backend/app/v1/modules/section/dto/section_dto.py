from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SectionDTO(BaseModel):
    """
    Represents a learning section returned to the client.

    A section is a navigable chapter within a learning topic.
    Educational content is stored separately as Blocks.
    """

    id: UUID

    title: str

    slug: str

    description: str | None

    order_index: int

    topic_id: UUID

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }