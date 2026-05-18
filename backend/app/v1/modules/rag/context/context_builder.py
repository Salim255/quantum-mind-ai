# rag/context/context_builder.py

from typing import List
# Type hint support for cleaner, more maintainable code.


# ------------------------------------------------------------------
# CONTEXT BUILDER
# ------------------------------------------------------------------
#
# PURPOSE
# -------
# This module prepares retrieved chunks before they are sent
# to the language model.
#
# WHY THIS STEP MATTERS
# ---------------------
# Retrieval alone is NOT enough for high-quality RAG.
#
# The way context is structured dramatically affects:
#
# - answer quality
# - hallucination rate
# - grounding
# - relevance
# - reasoning quality
#
# BAD CONTEXT BUILDING:
# - giant merged text blobs
# - duplicated chunks
# - messy formatting
# - no semantic separation
#
# GOOD CONTEXT BUILDING:
# - preserve chunk boundaries
# - preserve retrieval order
# - readable structure
# - clear semantic organization
#
# This file implements a clean educational RAG context builder.
# ------------------------------------------------------------------


def build_context(
    chunks: List[str],
    max_chars: int = 3000
) -> List[str]:
    """
    Build structured context for the LLM.

    PARAMETERS
    ----------
    chunks : List[str]
        Retrieved chunks from semantic search + reranking.

    max_chars : int
        Maximum total context size allowed.

        WHY LIMIT CONTEXT?
        ------------------
        Larger context:
        - increases token usage
        - increases cost
        - may confuse the LLM
        - may reduce answer precision

        Smaller focused context usually performs better.

    RETURNS
    -------
    List[str]
        A structured list of labeled chunks.

    WHY RETURN A LIST?
    ------------------
    Most prompt builders expect:
    - multiple context sections
    - not one giant merged string

    This preserves:
    - semantic boundaries
    - retrieval ranking
    - chunk separation
    """

    # --------------------------------------------------------------
    # Final selected chunks sent to the LLM.
    # --------------------------------------------------------------
    selected_chunks = []

    # --------------------------------------------------------------
    # Tracks total context size.
    # Prevents oversized prompts.
    # --------------------------------------------------------------
    total_chars = 0

    # --------------------------------------------------------------
    # Iterate over retrieved chunks in ranking order.
    #
    # IMPORTANT:
    # Retrieval order matters because:
    # - earlier chunks are usually more relevant
    # - reranking already optimized this ordering
    # --------------------------------------------------------------
    for index, chunk in enumerate(chunks):

        # Character length of the current chunk.
        chunk_length = len(chunk)

        # ----------------------------------------------------------
        # Stop if adding this chunk exceeds the allowed context size.
        #
        # This prevents:
        # - overly large prompts
        # - noisy context
        # - excessive token usage
        # ----------------------------------------------------------
        if total_chars + chunk_length > max_chars:
            break

        # ----------------------------------------------------------
        # Add explicit chunk labels.
        #
        # WHY LABEL CHUNKS?
        # -----------------
        # Labels help the LLM understand:
        #
        # - semantic separation
        # - chunk boundaries
        # - retrieval structure
        #
        # This often improves:
        # - grounding
        # - reasoning
        # - focused answering
        #
        # Example:
        #
        # [CONTEXT CHUNK 1]
        # Quantum computing uses qubits...
        # ----------------------------------------------------------
        labeled_chunk = (
            f"[CONTEXT CHUNK {index + 1}]\n"
            f"{chunk}"
        )

        # Store labeled chunk.
        selected_chunks.append(labeled_chunk)

        # Update current context size.
        total_chars += chunk_length

    # --------------------------------------------------------------
    # Return structured semantic context.
    # --------------------------------------------------------------
    return selected_chunks