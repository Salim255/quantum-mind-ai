# app/v1/modules/rag/dto/retrieval_dto.py

from typing import List, Optional
from pydantic import BaseModel


class RetrievedChunkDTO(BaseModel):
    text: str
    source: str
    concept: str
    cosine_score: float
    rerank_score: Optional[float] = None
    hybrid_score: Optional[float] = None


class RetrievalResponseDTO(BaseModel):
    query: str
    results: List[RetrievedChunkDTO]