from typing import Annotated
from fastapi import Depends
from app.v1.modules.rag.services.implementations.rag_service_impl import RAGServiceImpl
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.retriever.implementations.search_engine_impl import  RetrieverImpl
from app.v1.modules.rag.retriever.services.reranking_service import RerankingService
from app.core.container import Container
from fastapi import Request
from app.v1.modules.rag.retriever.services.embedding_service import EmbeddingService


# ------------------------------------------------------------
# CONTAINER DEPENDENCY
# ------------------------------------------------------------
def get_container(request: Request) -> Container:
    return request.app.state.container


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

def get_retriever_service(
        container: Annotated[Container, Depends(get_container)],
        reranking_service: Annotated[RerankingService, Depends(get_ranking_service)],
        embedding_service: Annotated[EmbeddingService, Depends(get_embedding_service)]
) -> RetrieverImpl:
    return RetrieverImpl(
        container=container,
        reranking_service=reranking_service,
        embedding_service=embedding_service
    )

def get_rag_service(
        container: Annotated[Container, Depends(get_container)],
        retriever_service: Annotated[RetrieverImpl, Depends(get_retriever_service)]
        ) -> RAGService:
    return RAGServiceImpl(
        retriever_service=retriever_service,
        container=container
        )
