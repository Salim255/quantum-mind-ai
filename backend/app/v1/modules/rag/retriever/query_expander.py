# app/v1/modules/rag/retriever/query_expander.py
from typing import List

def expand_query(query: str) -> List[str]:
    """
    QUERY EXPANSION ENGINE (CONCEPT-DRIVEN VERSION)
    ===============================================

    PURPOSE
    -------
    This service expands a user query into multiple semantic variants
    to improve retrieval recall in vector databases.

    WHY QUERY EXPANSION EXISTS
    --------------------------
    In real-world RAG systems, users rarely ask questions
    using the exact wording found in documents.

    Example:
        User query:
            "What is entanglement?"

        Document may contain:
            - "quantum correlation between particles"
            - "Bell state phenomenon"
            - "non-local quantum behavior"

    Without expansion → retrieval misses relevant chunks.
    With expansion → retrieval becomes robust.

    ------------------------------------------------------------
    DESIGN PRINCIPLE (VERY IMPORTANT)
    ------------------------------------------------------------
    ❌ BAD:
        Hardcoded keyword rules ("if quantum in query")

    ✅ GOOD:
        Use a centralized concept knowledge base (CONCEPTS)

    This ensures:
        - scalability
        - consistency with concept detection
        - easier maintenance
        - no duplicated logic
    """

    # ------------------------------------------------------------
    # STEP 1: ALWAYS KEEP ORIGINAL QUERY
    # ------------------------------------------------------------
    # WHY:
    # The original query is the most precise user intent signal.
    # It MUST always be part of retrieval input.
    # ------------------------------------------------------------
    expanded_queries: List[str] = [query]

    # Normalize query for matching (lowercase for robust comparison)
    q = query.lower()

    # ------------------------------------------------------------
    # STEP 2: CONCEPT-DRIVEN EXPANSION
    # ------------------------------------------------------------
    # WHY THIS EXISTS:
    # Instead of hardcoding rules per topic,
    # we reuse the CONCEPTS knowledge base.

    # Each concept contains:
    #   - anchors (strong semantic matches)
    #   - soft keywords (weak semantic signals)

    # This makes expansion:
    #   - scalable
    #   - consistent
    #   - reusable across retrieval + concept detection
    # ------------------------------------------------------------
    for concept_name, concept_data in CONCEPTS.items():

        # --------------------------------------------------------
        # CHECK IF QUERY BELONGS TO THIS CONCEPT
        # --------------------------------------------------------
        # We match against anchors because they represent
        # strong semantic identity of the concept.
        #
        # Example:
        #   "entanglement" → matches entanglement concept
        # --------------------------------------------------------
        if any(anchor in q for anchor in concept_data["anchors"]):

            # ----------------------------------------------------
            # STEP 2A: EXPAND USING STRONG SEMANTIC ANCHORS
            # ----------------------------------------------------
            # WHY:
            # Anchors represent core vocabulary used in documents.
            # Adding them improves retrieval recall significantly.
            # ----------------------------------------------------
            for anchor in concept_data["anchors"]:
                expanded_queries.append(anchor)

            # ----------------------------------------------------
            # STEP 2B: EXPAND USING SOFT SEMANTIC SIGNALS
            # ----------------------------------------------------
            # WHY:
            # Soft keywords capture paraphrases and intuition-level
            # descriptions often used in educational content.
            #
            # Example:
            #   "spooky action"
            #   "linked qubits"
            # ----------------------------------------------------
            for soft_keyword in concept_data.get("keywords_soft", []):
                expanded_queries.append(soft_keyword)

    # ------------------------------------------------------------
    # STEP 3: GENERAL EXPANSION FOR SHORT / VAGUE QUERIES
    # ------------------------------------------------------------
    # WHY THIS EXISTS:
    # Short queries like:
    #   "quantum"
    #   "entanglement"
    #
    # are too vague for precise retrieval.
    #
    # We generate interpretive forms to increase recall.
    # ------------------------------------------------------------
    if len(q.split()) <= 2:

        expanded_queries.extend([
            f"explain {q}",
            f"what is {q}",
            f"definition of {q}"
        ])

    # ------------------------------------------------------------
    # STEP 4: REMOVE DUPLICATES WHILE PRESERVING ORDER
    # ------------------------------------------------------------
    # WHY:
    # Expansion may generate repeated queries across:
    # - concepts
    # - anchors
    # - soft keywords
    #
    # dict.fromkeys() preserves insertion order
    # (important for deterministic retrieval behavior)
    # ------------------------------------------------------------
    expanded_queries = list(dict.fromkeys(expanded_queries))

    # ------------------------------------------------------------
    # FINAL OUTPUT
    # ------------------------------------------------------------
    # This list will be:
    #   1. embedded
    #   2. used for multi-query vector search
    #
    # Result:
    #   Higher recall + better semantic coverage
    # ------------------------------------------------------------
    return expanded_queries