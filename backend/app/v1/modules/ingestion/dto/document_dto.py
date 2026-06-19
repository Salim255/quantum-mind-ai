from typing import List, Optional
from pydantic import BaseModel


class MetadataDTO(BaseModel):
    source: str

    section_title: str

    concept: str

    length: int


class DocumentDTO(BaseModel):
    id: Optional[str] = None
    text: str
    embedding: List[float]
    metadata: MetadataDTO
    cosine_score: Optional[float] = None


class AddedDocResponseDto(BaseModel):
    status: str
    stored_text_length: int
    source: str