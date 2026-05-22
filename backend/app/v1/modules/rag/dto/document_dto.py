from typing import List
from pydantic import BaseModel


class MetadataDTO(BaseModel):
    source: str
    concept: str
    difficulty: str = "beginner"
    length: int


class DocumentDTO(BaseModel):
    text: str
    embedding: List[float]
    metadata: MetadataDTO


class AddedDocResponseDto(BaseModel):
    status: str
    stored_text_length: int
    source: str