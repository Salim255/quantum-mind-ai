from typing import List


def expand_query(query: str) -> List[str]:
    """
    Generate semantic variations of the user query.

    WHY?
    ----
    Users may phrase concepts differently than documents.

    Query expansion improves retrieval recall by searching
    multiple semantic variants of the same intent.
    """

    query_lower = query.lower()

    expansions = [query]

    # ------------------------------------------------------------
    # SIMPLE RULE-BASED EXPANSIONS
    # ------------------------------------------------------------

    if "qubit" in query_lower:
        expansions.extend([
            "quantum bit",
            "qubit state",
            "quantum computing qubit"
        ])

    if "entanglement" in query_lower:
        expansions.extend([
            "quantum entanglement",
            "entangled particles",
            "spooky action at a distance"
        ])

    if "superposition" in query_lower:
        expansions.extend([
            "quantum superposition",
            "multiple quantum states",
            "wave function state"
        ])

    # Remove duplicates while preserving order
    return list(dict.fromkeys(expansions))