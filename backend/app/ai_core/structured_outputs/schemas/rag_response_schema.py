from pydantic import BaseModel, Field
from typing import List

from app.ai_core.structured_outputs.schemas.rag_schema import RAGResponseSchema


# ------------------------------------------------------------
# FULL RAG API RESPONSE
# ------------------------------------------------------------
class RAGQueryResponseSchema(BaseModel):
    query: str
    retrieved_chunks: List[str] = Field(default_factory=list)

    final_answer: RAGResponseSchema

    source: List[str] = Field(default_factory=list)

    latency_ms: float = Field(default=0.0, description="Total latency of the RAG pipeline in milliseconds")