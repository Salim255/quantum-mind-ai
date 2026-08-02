from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from app.v1.modules.block.dto.block_type_dto import BlockTypeDTO


class BlockDTO(BaseModel):
    """
    Represents a learning block returned to the client.

    A block belongs to either:
    - a Topic (topic introduction), or
    - a Section (section content).
    """

    id: UUID

    title: str | None

    type: BlockTypeDTO

    content: str

    order_index: int

    topic_id: UUID | None

    section_id: UUID | None

    created_at: datetime

    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }