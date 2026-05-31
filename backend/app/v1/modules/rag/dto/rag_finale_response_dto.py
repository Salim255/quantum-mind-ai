from pydantic import BaseModel, Field
from typing import List

from app.v1.modules.rag.dto.rag_response_dto import RAGResponseDto
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

# ------------------------------------------------------------
# FULL RAG API RESPONSE
# ------------------------------------------------------------
class RAGQueryFinaleResponseDto(BaseModel):
    query: str
    
    retrieved_chunks: List[RetrievalChunkDTO] = Field(default_factory=list)

    final_answer: RAGResponseDto

    latency_ms: float = Field(default=0.0, description="Total latency of the RAG pipeline in milliseconds")