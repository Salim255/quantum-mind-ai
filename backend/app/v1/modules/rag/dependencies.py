from typing import Annotated
from fastapi import Depends
from app.v1.modules.rag.services.implementations.rag_service_impl import RAGServiceImpl
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.vector_store.add_document import RAGAddDocument
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.v1.modules.rag.search_engine.implementations.search_engine_impl import SearchEngineImpl
from app.v1.modules.rag.search_engine.services.reranking_service import RerankingService
from app.core.container import Container
from fastapi import Request
from app.v1.modules.rag.search_engine.services.embedding_service import EmbeddingService


# ------------------------------------------------------------
# CONTAINER DEPENDENCY
# ------------------------------------------------------------
def get_container(request: Request) -> Container:
    return request.app.state.container

def get_add_document_service(
        container: Annotated[Container, Depends(get_container)]
    ) -> RAGAddDocument:
    return  RAGAddDocument(container=container)

def get_ranking_service(
        container: Annotated[Container, Depends(get_container)]
) -> RerankingService:
    return RerankingService(container=container)

def get_embedding_service(
        container: Annotated[Container, Depends(get_container)]
) -> EmbeddingService:
    return EmbeddingService(
        container=container
    )

def get_search_engine_service(
        container: Annotated[Container, Depends(get_container)],
        reranking_service: Annotated[RerankingService, Depends(get_ranking_service)],
        embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)]
) -> SearchEngineImpl:
    return SearchEngineImpl(
        container=container,
        reranking_service=reranking_service,
        embedding_service=embedding_service
    )

def get_rag_service(
        container: Annotated[Container, Depends(get_container)],
        search_engine_service: Annotated[SearchEngineImpl, Depends(get_search_engine_service)]
        ) -> RAGService:
    return RAGServiceImpl(
        search_engine_service=search_engine_service,
        container=container
        )

def get_loader_service(
        container: Annotated[Container, Depends(get_container)],
        add_document_service: Annotated[RAGAddDocument, Depends(get_add_document_service)]
) -> LoaderService:
    return LoaderServiceImpl(
        container=container,
        add_document_service=add_document_service
    )
