from typing import Annotated
from fastapi import Depends
from app.v1.modules.rag.services.implementations.rag_service_impl import RAGServiceImpl
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.v1.modules.rag.search_engine.implementations.search_engine_impl import SearchEngineImpl
from app.core.container import Container

def get_search_engine_service() -> SearchEngineImpl:
    return SearchEngineImpl()

def get_rag_service(
        search_engine_service: Annotated[SearchEngineImpl, Depends(get_search_engine_service)]
        ) -> RAGService:
    return RAGServiceImpl(
        search_engine_service=search_engine_service,
        settings=Container.settings
        )

def get_loader_service() -> LoaderService:
    return LoaderServiceImpl()

