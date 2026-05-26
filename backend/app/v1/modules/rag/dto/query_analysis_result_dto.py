from dataclasses import dataclass


@dataclass
class QueryAnalysisResultDto:
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