from fastapi import (APIRouter, Depends, File, UploadFile)
from typing import Annotated
from pydantic import BaseModel
from app.v1.modules.rag.dto.rag_finale_response_dto import RAGQueryFinaleResponseDto
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.rag.dto.ingestion_dto import IngestionResponseDto
from app.v1.modules.rag.dependencies import get_loader_service
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService


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

@router.post("/ingest-pdf")
async def ingest_pdf(
    file: Annotated[UploadFile, File(...)],
    loader_service: Annotated[LoaderService, Depends(get_loader_service)]
) -> IngestionResponseDto:
    return await loader_service.upload_and_ingest_pdf(file)