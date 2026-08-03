from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class SectionDTO(BaseModel):
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
