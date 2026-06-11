from app.v1.modules.learn.service.learn_impl_service import LearnImplService
from app.v1.modules.learn.service.learn_service import LearnService
from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService
from app.v1.modules.learn.service.topic_ingestion_impl_service import TopicIngestionImplService
from app.v1.modules.learn.service.doc_ingestion_impl_service import DocIngestionImplService
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService
from app.v1.modules.learn.service.doc_ingestion_impl_service_v2 import DocIngestionImplServiceV2
from app.v1.modules.learn.service.doc_ingestion_service_v2 import DocIngestionServiceV2

def get_doc_ingestion_service_v2() -> DocIngestionServiceV2:
    return  DocIngestionImplServiceV2()

def get_doc_ingestion_service() -> DocIngestionService:
    return DocIngestionImplService()

def get_learn_service() -> LearnService:
    return LearnImplService()

def get_topic_ingestion_service() -> TopicIngestionService:
    return TopicIngestionImplService()