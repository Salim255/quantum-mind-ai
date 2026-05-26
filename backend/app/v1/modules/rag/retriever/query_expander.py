# app/v1/modules/rag/retriever/query_expander.py

from typing import List


def expand_query(query: str) -> List[str]:
    """
    QUERY EXPANSION LAYER

    PURPOSE
    -------
    Improves retrieval recall by generating multiple
    semantic variations of the user's query.

    WHY IMPORTANT?
    --------------
    Users may ask the same concept in different ways.

    Example:
    --------
    Original:
        "What is entanglement?"

    Expanded:
        - "Explain quantum entanglement"
        - "Definition of entanglement"
        - "How do entangled particles work"

    This increases the chance of retrieving:
    - differently worded chunks
    - hidden semantic matches
    - better educational context

    CURRENT VERSION
    ---------------
    Right now this is rule-based/simple expansion.

    LATER YOU CAN UPGRADE TO:
    -------------------------
    - LLM-generated expansions
    - HyDE retrieval
    - synonym generation
    - domain-aware reformulation
    - multilingual retrieval

    PARAMETERS
    ----------
    query : str
        Original user query.

    RETURNS
    -------
    List[str]
        List of expanded semantic queries.
    """

    # ------------------------------------------------------------
    # START WITH ORIGINAL QUERY
    # ------------------------------------------------------------
    # Always preserve the user's original wording.
    # This remains the primary retrieval anchor.
    # ------------------------------------------------------------
    expanded_queries = [query]

    q = query.lower()

    # ------------------------------------------------------------
    # QUANTUM-SPECIFIC EXPANSIONS
    # ------------------------------------------------------------
    # Add semantic variations for known concepts.
    #
    # WHY?
    # ----
    # Educational PDFs may describe concepts
    # using different terminology.
    # ------------------------------------------------------------
     # ============================================================
    # 1. DOMAIN-LEVEL EXPANSION (IMPORTANT FIX)
    # ============================================================
    # This fixes:
    #   "what is quantum?"
    #   "quantum?"
    #   "explain quantum"
    # ============================================================
    if "quantum" in q:

        expanded_queries.extend([
            "quantum computing basics",
            "introduction to quantum mechanics",
            "qubits superposition entanglement measurement",
            "quantum state explanation",
            "how quantum computing works"
        ])

    # ------------------------------------------------------------
    # ENTANGLEMENT
    # ------------------------------------------------------------
    if "entanglement" in q:

        expanded_queries.extend([
            "Explain quantum entanglement",
            "Definition of entanglement",
            "How entangled particles behave",
            "Quantum correlation between particles"
        ])

    # ------------------------------------------------------------
    # SUPERPOSITION
    # ------------------------------------------------------------
    if "superposition" in q:

        expanded_queries.extend([
            "Explain quantum superposition",
            "Quantum state combination",
            "Particle existing in multiple states",
            "Definition of superposition"
        ])

    # ------------------------------------------------------------
    # QUBITS
    # ------------------------------------------------------------
    if "qubit" in q or "qubits" in q:

        expanded_queries.extend([
            "Explain qubits",
            "Quantum computing bit",
            "Difference between bit and qubit",
            "Quantum information unit"
        ])

    # ------------------------------------------------------------
    # MEASUREMENT
    # ------------------------------------------------------------
    if "measurement" in q:

        expanded_queries.extend([
            "Quantum measurement collapse",
            "Wave function collapse",
            "Observation in quantum mechanics",
            "Measurement of quantum states"
        ])

    # ------------------------------------------------------------
    # REMOVE DUPLICATES
    # ------------------------------------------------------------
    # dict.fromkeys preserves order while removing duplicates.
    # ------------------------------------------------------------
    expanded_queries = list(dict.fromkeys(expanded_queries))

    return expanded_queries