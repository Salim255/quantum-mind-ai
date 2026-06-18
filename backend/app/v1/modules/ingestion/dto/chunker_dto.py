# rag/dto/chunk_dto.py
from pydantic import BaseModel


class ChunkDTO(BaseModel):
    content: str

    concept: str

    length: int


    bookmark_title: str

    order: int

    source_name: str | None = None