# rag/dto/chunk_dto.py
from pydantic import BaseModel


class ChunkDTO(BaseModel):
    text: str
    concept: str
    length: int
