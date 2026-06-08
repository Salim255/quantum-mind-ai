from app.v1.modules.learn.service.learn_impl_service import LearnImplService
from app.v1.modules.learn.service.learn_service import LearnService
from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService
from app.v1.modules.learn.service.topic_ingestion_impl_service import TopicIngestionImplService

def get_learn_service() -> LearnService:
    return LearnImplService()

def get_topic_ingestion_service() -> TopicIngestionService:
    return TopicIngestionImplService()