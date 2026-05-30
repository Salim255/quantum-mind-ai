from pydantic import BaseModel
from typing import List


class PointDTO(BaseModel):
    id: str

    text: str
    
    source: str

    concept: str

    difficulty: str = "beginner"

    length: int

    vector: List[float]

    # Original Qdrant similarity score
    qdrant_score: float