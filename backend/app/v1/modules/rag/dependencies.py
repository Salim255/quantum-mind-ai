from typing import Annotated
from fastapi.params import Depends

from app.v1.modules.rag.services.implementations.rag_service_impl import RAGServiceImpl
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.core.settings import Settings, get_settings


def get_rag_service(
        settings: Annotated[Settings, Depends(get_settings)]) -> RAGService:
    return RAGServiceImpl(
        settings=settings
        )
