from typing import Annotated
from app.v1.modules.ingestion.service.ingestion_impl_service import DocIngestionImplService
from app.v1.modules.ingestion.service.ingestion_service import DocIngestionService
from app.core.container import Container
from fastapi import Request, Depends

# ------------------------------------------------------------
# CONTAINER DEPENDENCY
# ------------------------------------------------------------
def get_container(request: Request) -> Container:
    return request.app.state.container

def get_doc_ingestion_service(
        container: Annotated[Container, Depends(get_container)]
    ) -> DocIngestionService:
    return DocIngestionImplService(container=container)
