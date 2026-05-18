from fastapi import (APIRouter, Depends)
from typing import Annotated

from pydantic import BaseModel
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema
from app.ai_core.structured_outputs.schemas.rag_eval_schema import RAGEvaluationLog, RetrievedChunk
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service


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