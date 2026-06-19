# rag/dto/chunk_dto.py
from pydantic import BaseModel


class ChunkDTO(BaseModel):
    chapter_title: str

    section_title: str
    
    content: str

    length: int

    order: int

    source_name: str | None = None