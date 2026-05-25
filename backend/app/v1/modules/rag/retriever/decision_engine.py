# ------------------------------------------------------------
# CONFIDENCE THRESHOLDS (DECISION LAYER)
# ------------------------------------------------------------
# These control how the system behaves after retrieval.
#
# They replace simple "if score < threshold" logic
# with multi-level reasoning.
# ------------------------------------------------------------

HIGH_CONFIDENCE = 5.0
MEDIUM_CONFIDENCE = 2.5
LOW_CONFIDENCE = 1.0


from enum import Enum


class RetrievalAction(str, Enum):
    """
    Decision outcomes for the retrieval pipeline.

    This controls what the RAG system should do
    after evaluating retrieval confidence.
    """

    # ------------------------------------------------------------
    # NO_RESULT
    # ------------------------------------------------------------
    # No relevant context found in vector DB.
    #
    # → Generator should refuse or say:
    #   "I don't have enough information."
    # ------------------------------------------------------------
    NO_RESULT = "NO_RESULT"

    # ------------------------------------------------------------
    # CLARIFY
    # ------------------------------------------------------------
    # Query is too ambiguous.
    #
    # → System should ask user a follow-up question.
    # ------------------------------------------------------------
    CLARIFY = "CLARIFY"

    # ------------------------------------------------------------
    # RETRY
    # ------------------------------------------------------------
    # Retrieval is weak but salvageable.
    #
    # → System should expand query or re-run retrieval.
    # ------------------------------------------------------------
    RETRY = "RETRY"

    # ------------------------------------------------------------
    # OK
    # ------------------------------------------------------------
    # Retrieval is strong enough to answer directly.
    # ------------------------------------------------------------
    OK = "OK"

def decide_retrieval_action(best_score: float) -> RetrievalAction:
    """
    Determines system behavior based on retrieval confidence.

    Returns
    -------
    str : one of
        - "ANSWER"
        - "RETRY"
        - "CLARIFY"
        - "NO_RESULT"
    """
    # ------------------------------------------------------------
    # CASE 1: STRONG SIGNAL
    # ------------------------------------------------------------
    if best_score >= HIGH_CONFIDENCE:
        return  RetrievalAction.OK

    # ------------------------------------------------------------
    # CASE 2: MODERATE SIGNAL
    # ------------------------------------------------------------
    if best_score >= MEDIUM_CONFIDENCE:
        return  RetrievalAction.RETRY

    # ------------------------------------------------------------
    # CASE 3: WEAK SIGNAL
    # ------------------------------------------------------------
    if best_score >= LOW_CONFIDENCE:
        return  RetrievalAction.CLARIFY

    # ------------------------------------------------------------
    # CASE 4: NO MEANINGFUL MATCH
    # ------------------------------------------------------------
    return  RetrievalAction.NO_RESULT