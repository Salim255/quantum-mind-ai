from pydantic import BaseModel
from typing import List, Optional


class RAGResponseSchema(BaseModel):
    """
    Standard output format for ALL RAG queries.
    This is the contract between LLM and API.
    """

    # Final answer (must be grounded in context)
    answer: str

    # Key extracted facts (no formatting, no markdown)
    key_points: List[str] = []

    # Step-by-step explanation (only if useful)
    step_by_step: List[str] = []

    # Simple analogy (optional but helpful for learning queries)
    analogy: Optional[str] = ""

    # Model confidence (0.0 → 1.0)
    confidence: float = 0.0

    # Optional: traceability to chunks
    sources: List[str] = []