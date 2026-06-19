from fastapi import (APIRouter, Depends, File, UploadFile)
from typing import Annotated
from pydantic import BaseModel
from app.v1.modules.rag.dto.rag_finale_response_dto import RAGQueryFinaleResponseDto
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.rag.dto.ingestion_dto import IngestionResponseDto

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def rag_query(
    payload: QueryRequest,
    rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> RAGQueryFinaleResponseDto:
    return rag_service.rag_pipeline(payload)