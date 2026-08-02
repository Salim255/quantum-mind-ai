
from app.v1.modules.topic.service.topic_service import TopicService
from app.v1.modules.topic.service.topic_impl_service import TopicImplService

def get_topic_service() -> TopicService:
    return TopicImplService()