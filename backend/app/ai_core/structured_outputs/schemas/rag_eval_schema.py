# rag_eval_schema.py
# ---------------------------------------------------------
# PURPOSE
# -------
# Store evaluation data for every RAG request.
#
# WHY THIS MATTERS
# ----------------
# RAG systems are difficult to improve blindly.
#
# Logging lets us measure:
# - retrieval quality
# - reranking quality
# - hallucinations
# - latency
# - chunk usefulness
#
# This schema becomes the foundation
# of the RAG evaluation dashboard.
# ---------------------------------------------------------

from typing import List, Optional
from pydantic import BaseModel


class RetrievedChunk(BaseModel):
    """
    Represents a retrieved chunk used during RAG.
    """

    text: str
    source: str
    score: Optional[float] = None


class RAGEvaluationLog(BaseModel):
    """
    Full evaluation log for a single RAG query.
    """

    # -----------------------------------------------------
    # USER INPUT
    # -----------------------------------------------------
    query: str

    # -----------------------------------------------------
    # RETRIEVAL
    # -----------------------------------------------------
    retrieved_chunks: List[RetrievedChunk]

    # -----------------------------------------------------
    # FINAL GENERATED ANSWER
    # -----------------------------------------------------
    final_answer: dict

    # -----------------------------------------------------
    # PERFORMANCE
    # -----------------------------------------------------
    latency_ms: float

    # -----------------------------------------------------
    # MODEL INFO
    # -----------------------------------------------------
    model: str

    # -----------------------------------------------------
    # OPTIONAL METADATA
    # -----------------------------------------------------
    top_k: int