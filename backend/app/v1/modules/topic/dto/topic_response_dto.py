
from pydantic import BaseModel
from app.v1.modules.topic.dto.topic_dto import TopicDTO, TopicOnlyDTO


class TopicResponseDTO(BaseModel):
    """
    DTO returned when reading a QuantumMind learning topic.

    Represents the public topic information exposed by the API.

    This DTO is used for:
    - Created topic responses
    - Topic details pages
    - Topic listings

    Database-only fields are intentionally excluded.
    """
    topic: TopicDTO | TopicOnlyDTO