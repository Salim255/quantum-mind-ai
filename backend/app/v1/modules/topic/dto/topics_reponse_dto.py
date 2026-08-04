
from pydantic import BaseModel

from app.v1.modules.topic.dto.topic_dto import TopicDTO


class TopicsResponseDTO(BaseModel):
    """
    Response DTO for topics.
    """
    topics: list[TopicDTO]