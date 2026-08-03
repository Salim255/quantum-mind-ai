from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.v1.modules.block.dto.block_type_dto import BlockTypeDTO


class BlockDTO(BaseModel):
    """
    Represents a learning content block.

    A block belongs to either:
    - a Topic (topic-level introduction)
    - a Section (section-level content)
    """

    model_config = ConfigDict(
        from_attributes=True
    )

    id: UUID

    type: BlockTypeDTO

    content: str

    display_order: int

    topic_id: UUID | None = None

    section_id: UUID | None = None

    created_at: datetime

    updated_at: datetime