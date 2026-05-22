from typing import Optional, List
from pydantic import BaseModel


class RerankDocumentDTO(BaseModel):
    text: str
    cosine_score: Optional[float] = 0.0
    rerank_score: Optional[float] = None



class RerankResponseDTO(BaseModel):
    documents: List[RerankDocumentDTO]