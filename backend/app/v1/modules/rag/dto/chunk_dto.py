# rag/dto/chunk_dto.py

from typing import List, Optional
from pydantic import BaseModel


class ChunkCandidateDTO(BaseModel):
    text: str
    source: str = "unknown"
    concept: str = "unknown"
    length: int = 0

    cosine_score: float = 0.0
    rerank_score: Optional[float] = None
    hybrid_score: Optional[float] = None