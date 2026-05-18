from fastapi import (APIRouter, Depends, File, UploadFile)
from typing import Annotated

from pydantic import BaseModel
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema
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
) -> RAGQueryResponseSchema:
    return rag_service.rag_pipeline(payload)

@router.post("/ingest-pdf")
async def ingest_pdf(
    file: Annotated[UploadFile, File(...)],
    loader_service: Annotated[LoaderService, Depends(get_loader_service)]
) -> IngestionResponseSchema:
    return await loader_service.upload_and_ingest_pdf(file)