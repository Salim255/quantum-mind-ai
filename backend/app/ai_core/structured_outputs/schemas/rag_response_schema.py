from pydantic import BaseModel, Field
from typing import List


# ------------------------------------------------------------
# LLM FINAL ANSWER STRUCTURE
# ------------------------------------------------------------
class RAGFinalAnswerSchema(BaseModel):
    answer: str = Field(..., description="Final generated answer")
    key_points: List[str] = Field(default_factory=list)
    step_by_step: List[str] = Field(default_factory=list)
    analogy: str | None = None
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)


# ------------------------------------------------------------
# FULL RAG API RESPONSE
# ------------------------------------------------------------
class RAGQueryResponseSchema(BaseModel):
    query: str
    retrieved_chunks: List[str] = Field(default_factory=list)

    final_answer: RAGFinalAnswerSchema

    source: List[str] = Field(default_factory=list)

    latency_ms: float | None = None