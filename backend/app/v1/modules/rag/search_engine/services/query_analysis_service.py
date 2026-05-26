import re
from dataclasses import dataclass


@dataclass
class QueryAnalysisResult:
    """
    STRUCTURED OUTPUT OF QUERY UNDERSTANDING

    WHY THIS EXISTS:
    ----------------
    We don't just return a label.
    We return a full retrieval "decision object"
    that downstream services can use.
    """
    query_type: str
    is_broad: bool
    is_specific: bool
    is_question: bool
    requires_expansion: bool
    cleaned_query: str

class QueryAnalysisService:
    """
    QUERY ANALYSIS SERVICE (RAG RETRIEVAL BRAIN LAYER)
    ===================================================

    PURPOSE
    -------
    Classify user query BEFORE retrieval.

    WHY THIS IS CRITICAL
    --------------------
    Without query understanding:
    - all queries are treated the same
    - broad queries fail ("Quantum?")
    - retrieval becomes unstable
    """

    # ------------------------------------------------------------
    # NORMALIZATION
    # ------------------------------------------------------------
    @staticmethod
    def normalize(query: str) -> str:
        """
        WHY:
        Clean query for consistent analysis.

        WHAT IT SOLVES:
        - case inconsistency
        - extra spaces
        - punctuation noise
        """
        return re.sub(r"\s+", " ", query.lower().strip())
    def detect():
