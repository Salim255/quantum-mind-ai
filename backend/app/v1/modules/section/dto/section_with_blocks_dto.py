
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.v1.modules.block.dto.block_dto import BlockDTO
from pydantic import ConfigDict
from typing import List

class SectionWithBlocksDTO(BaseModel):
    """
    Data Transfer Object for a Section along with its associated Blocks.
    """
    id: UUID
    title: str
    slug: str
    description: str | None
    order_index: int
    topic_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )

    blocks: List[BlockDTO] = []