# rag/context/context_builder.py

from typing import List
# Type hint support for cleaner, more maintainable code.
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

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

def assign_context_role(index: int) -> str:
    """
    Assigns reasoning role based on ranking position.
    """

    # Top chunk = main answer signal
    if index == 0:
        return "core"

    # Second chunk = explanation support
    if index == 1:
        return "supporting"

    # Lower chunks = examples / edge cases
    return "example"

def build_reasoned_context(
    chunks: List[RetrievalChunkDTO],
    max_chars: int = 3000
) -> str:
    """
    Builds structured reasoning context with strict size control.

    WHY THIS MATTERS
    ----------------
    Prevents:
    - Groq token overflow (TPM errors)
    - excessive prompt cost
    - noisy context injection

    Ensures:
    - structured reasoning order
    - safe LLM input size
    """

    sections = {
        "core": [],
        "supporting": [],
        "example": []
    }

    # ------------------------------------------------------------
    # 1. GROUP BY ROLE
    # ------------------------------------------------------------
    for chunk in chunks:
        role = getattr(chunk, "context_role", "supporting")
        sections[role].append(chunk)

    context_parts = []
    total_chars = 0

    # ------------------------------------------------------------
    # 2. ORDERED INSERTION (core → support → examples)
    # ------------------------------------------------------------

    ordered_roles = ["core", "supporting", "example"]

    for role in ordered_roles:

        for c in sections[role]:

            block = f"[{role.upper()}]\n{c.text}\n\n"
            block_len = len(block)

            # ----------------------------------------------------
            # 3. HARD LIMIT CHECK
            # ----------------------------------------------------
            if total_chars + block_len > max_chars:
                return "".join(context_parts).strip()

            context_parts.append(block)
            total_chars += block_len

    return "".join(context_parts).strip()

def build_context(
    chunks: List[RetrievalChunkDTO],
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
        chunk_length = len(chunk.text)

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
            f"{chunk.text}"
        )

        # Store labeled chunk.
        selected_chunks.append(labeled_chunk)

        # Update current context size.
        total_chars += chunk_length

    # --------------------------------------------------------------
    # Return structured semantic context.
    # --------------------------------------------------------------
    return selected_chunks