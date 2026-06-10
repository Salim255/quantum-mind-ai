from app.v1.modules.learn.service.learn_impl_service import LearnImplService
from app.v1.modules.learn.service.learn_service import LearnService
from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService
from app.v1.modules.learn.service.topic_ingestion_impl_service import TopicIngestionImplService
from app.v1.modules.learn.service.doc_ingestion_impl_service import DocIngestionImplService
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService

def get_doc_ingestion_service() -> DocIngestionService:
    return DocIngestionImplService()

def get_learn_service() -> LearnService:
    return LearnImplService()

def get_topic_ingestion_service() -> TopicIngestionService:
    return TopicIngestionImplService()