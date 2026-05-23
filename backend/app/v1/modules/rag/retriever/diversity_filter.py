from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO


def is_similar(a: str, b: str, threshold: float = 0.92) -> bool:
    """
    Lightweight semantic duplication check.

    NOTE:
    In production you can replace this with:
    - embedding similarity
    - or MinHash / cosine similarity
    """

    return a.strip().lower() == b.strip().lower()