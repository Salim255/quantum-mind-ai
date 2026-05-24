from app.v1.modules.rag.services.implementations.rag_service_impl import RAGServiceImpl
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.core.container import Container

def get_rag_service() -> RAGService:
    return RAGServiceImpl(
        settings=Container.settings
        )

def get_loader_service() -> LoaderService:
    return LoaderServiceImpl()