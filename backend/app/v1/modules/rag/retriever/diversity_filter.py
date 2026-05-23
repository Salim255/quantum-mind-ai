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

def diversify_results(
    chunks: List[RetrievalChunkDTO],
    max_per_concept: int = 1,
    top_k: int = 3
) -> List[RetrievalChunkDTO]:
    """
    Selects diverse, non-redundant top-k results.

    Goals:
    - avoid duplicates
    - ensure concept diversity
    - preserve ranking quality
    """

    selected = []
    seen_texts = set()
    concept_count = {}

    for chunk in chunks:

        text_key = chunk.text.strip().lower()
        concept = (chunk.concept or "unknown").lower()

        # --------------------------------------------------------
        # 1. HARD DEDUPLICATION
        # --------------------------------------------------------
        if text_key in seen_texts:
            continue

        # --------------------------------------------------------
        # 2. CONCEPT LIMIT
        # --------------------------------------------------------
        if concept_count.get(concept, 0) >= max_per_concept:
            continue

        # --------------------------------------------------------
        # ACCEPT CHUNK
        # --------------------------------------------------------
        selected.append(chunk)
        seen_texts.add(text_key)
        concept_count[concept] = concept_count.get(concept, 0) + 1

        # --------------------------------------------------------
        # STOP CONDITION
        # --------------------------------------------------------
        if len(selected) >= top_k:
            break

    return selected