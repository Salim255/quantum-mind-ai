from pydantic import BaseModel, Field
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

    results: List[str] = Field(default_factory=[], description="List of retrieved semantic chunks relevant to the query")

    sources: List[str] = Field(default_factory=[], description="List of sources associated with each retrieved chunk")