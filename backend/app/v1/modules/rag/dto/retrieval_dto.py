# app/v1/modules/rag/dto/retrieval_dto.py

from typing import List, Optional
from pydantic import BaseModel, Field


class RetrievalChunkDTO(BaseModel):
    text: str
    source: str
    concept: str
    length: int = Field(default_factory=0, description="text length")
    cosine_score: float
    rerank_score: Optional[float] = None
    hybrid_score: Optional[float] = None


class RetrievalResponseDTO(BaseModel):
    results: List[RetrievalChunkDTO] = Field(default_factory=[], description="List of retrieved semantic chunks relevant to the query")