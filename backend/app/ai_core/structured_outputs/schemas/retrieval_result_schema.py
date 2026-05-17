from pydantic import BaseModel
from typing import List


class RetrievalResultSchema(BaseModel):
    """
    Structured output of the retrieval pipeline.

    This object represents the final retrieval results
    returned after:
    - semantic search
    - cosine similarity
    - reranking

    Fields
    ------
    results:
        Retrieved semantic chunks.

    sources:
        Sources associated with each chunk.
    """

    results: List[str]

    sources: List[str]