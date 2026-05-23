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

def decide_retrieval_action(best_score: float) -> str:
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
        return "ANSWER"

    # ------------------------------------------------------------
    # CASE 2: MODERATE SIGNAL
    # ------------------------------------------------------------
    if best_score >= MEDIUM_CONFIDENCE:
        return "RETRY"

    # ------------------------------------------------------------
    # CASE 3: WEAK SIGNAL
    # ------------------------------------------------------------
    if best_score >= LOW_CONFIDENCE:
        return "CLARIFY"

    # ------------------------------------------------------------
    # CASE 4: NO MEANINGFUL MATCH
    # ------------------------------------------------------------
    return "NO_RESULT"