import re
from app.v1.modules.rag.dto.query_analysis_result_dto import QueryAnalysisResultDto

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
    
        # ------------------------------------------------------------
    # MAIN ENTRY POINT
    # ------------------------------------------------------------
    @classmethod
    def detect(cls, query: str) -> QueryAnalysisResultDto:
        """
        ANALYZE QUERY TYPE FOR RETRIEVAL STRATEGY
        """

        q = cls.normalize(query)

        # --------------------------------------------------------
        # BASIC SIGNALS
        # --------------------------------------------------------
        is_question = "?" in query or any(
            w in q for w in ["what", "how", "why", "explain", "define"]
        )

        token_count = len(q.split())

        # --------------------------------------------------------
        # 1. BROAD QUERY DETECTION
        # --------------------------------------------------------
        # WHY THIS EXISTS:
        # Queries like:
        # - "Quantum"
        # - "Physics"
        # need expansion across multiple concepts
        is_broad = (
            token_count <= 2 and
            len(q) <= 15
        )

        # --------------------------------------------------------
        # 2. SPECIFIC QUERY DETECTION
        # --------------------------------------------------------
        # WHY:
        # More precise queries map to a single concept
        is_specific = (
            token_count >= 3 or
            any(keyword in q for keyword in [
                "explain", "how does", "what is"
            ])
        )

        # --------------------------------------------------------
        # 3. EXPANSION DECISION
        # --------------------------------------------------------
        # WHY:
        # We only expand when needed to avoid noise explosion
        requires_expansion = is_broad or is_question

        # --------------------------------------------------------
        # 4. QUERY TYPE CLASSIFICATION
        # --------------------------------------------------------
        if is_broad:
            query_type = "broad"
        elif is_specific:
            query_type = "specific"
        else:
            query_type = "keyword"

        # --------------------------------------------------------
        # OUTPUT STRUCTURE
        # --------------------------------------------------------
        return QueryAnalysisResultDto(
            query_type=query_type,
            is_broad=is_broad,
            is_specific=is_specific,
            is_question=is_question,
            requires_expansion=requires_expansion,
            cleaned_query=q
        )
