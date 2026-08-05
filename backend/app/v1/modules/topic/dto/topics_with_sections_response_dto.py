
from pydantic import BaseModel

from app.v1.modules.topic.dto.topic_with_sections_dto import TopicWithSectionsDTO

class TopicsWithSectionsResponseDTO(BaseModel):
    """
    Response DTO for topics.
    """

    topics: list[TopicWithSectionsDTO ]