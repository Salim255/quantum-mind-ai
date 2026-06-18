from app.v1.modules.ingestion.service.ingestion_impl_service import DocIngestionImplService
from app.v1.modules.ingestion.service.ingestion_service import DocIngestionService


def get_doc_ingestion_service() -> DocIngestionService:
    return DocIngestionImplService()
