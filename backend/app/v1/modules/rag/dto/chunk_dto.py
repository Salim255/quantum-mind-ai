# rag/dto/chunk_dto.py

from typing import List, Optional
from pydantic import BaseModel


class ChunkDTO(BaseModel):
    text: str
    concept: str
    length: int