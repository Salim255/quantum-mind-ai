# rag/loader/chunker.py
# ------------------------------------------------------------------
# SEMANTIC CHUNKER FOR EDUCATIONAL RAG SYSTEMS
# ------------------------------------------------------------------
#
# PURPOSE
# -------
# This module transforms large educational text into smaller,
# semantically meaningful chunks.
#
# These chunks are later:
# - embedded into vectors
# - stored in the vector database
# - retrieved during semantic search
#
# WHY CHUNKING MATTERS
# --------------------
# Large language models and embedding models work best when text is:
#
# - coherent
# - focused
# - semantically meaningful
#
# BAD CHUNKS:
# - broken words
# - mixed topics
# - random character slices
# - isolated fragments
#
# GOOD CHUNKS:
# - one idea
# - one explanation
# - one concept
# - meaningful educational context
#
# This file implements a production-style semantic chunking pipeline.
# ------------------------------------------------------------------

import re
# Python regular expression module.
# Used for:
# - whitespace normalization
# - sentence splitting
# - cleanup operations

from typing import List
# Type hint support for cleaner, safer code.


# ------------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------------

def semantic_chunk_text(
    text: str,
    max_chars: int = 1200,
    overlap_sentences: int = 2
) -> List[str]:
    """
    Main semantic chunking pipeline.

    PARAMETERS
    ----------
    text : str
        The normalized educational text.

    max_chars : int
        Maximum approximate chunk size.

    overlap_sentences : int
        Number of sentences preserved between chunks.

    RETURNS
    -------
    List[str]
        List of semantic chunks.

    PIPELINE
    --------
    1. Normalize text
    2. Split into paragraphs
    3. Build semantic chunks
    4. Clean final chunks
    """

    # --------------------------------------------------------------
    # STEP 1:
    # Normalize spacing while preserving structure.
    # --------------------------------------------------------------
    normalized = normalize_chunk_text(text)

    # --------------------------------------------------------------
    # STEP 2:
    # Split into semantic paragraphs.
    # --------------------------------------------------------------
    paragraphs = split_into_paragraphs(normalized)

    # --------------------------------------------------------------
    # STEP 3:
    # Build semantic chunks from sentence groups.
    # --------------------------------------------------------------
    chunks = build_semantic_chunks(
        paragraphs,
        max_chars,
        overlap_sentences
    )

    # --------------------------------------------------------------
    # STEP 4:
    # Final cleanup + noise filtering.
    # --------------------------------------------------------------
    return cleanup_chunks(chunks)


# ------------------------------------------------------------------
# TEXT NORMALIZATION
# ------------------------------------------------------------------

def normalize_chunk_text(text: str) -> str:
    """
    Normalize whitespace while preserving semantic structure.

    IMPORTANT:
    We preserve paragraph boundaries because they help
    maintain semantic meaning during chunking.
    """

    # Replace repeated spaces/tabs with a single space.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive empty lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# ------------------------------------------------------------------
# PARAGRAPH SPLITTING
# ------------------------------------------------------------------

def split_into_paragraphs(text: str) -> List[str]:
    """
    Split text into paragraphs.

    WHY PARAGRAPHS?
    ---------------
    Paragraphs often naturally represent:
    - one concept
    - one explanation
    - one educational idea

    This makes them ideal semantic boundaries.
    """

    return [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]


# ------------------------------------------------------------------
# SENTENCE SPLITTING
# ------------------------------------------------------------------

def split_into_sentences(paragraph: str) -> List[str]:
    """
    Split a paragraph into sentences.

    REGEX EXPLANATION
    -----------------
    (?<=[.!?])\\s+

    Means:
    - split AFTER punctuation
    - split on following whitespace

    Example:
    --------
    Input:
        "Quantum is fascinating. Qubits are powerful."

    Output:
        [
            "Quantum is fascinating.",
            "Qubits are powerful."
        ]
    """

    sentences = re.split(
        r'(?<=[.!?])\s+',
        paragraph
    )

    # Remove empty sentences.
    return [
        s.strip()
        for s in sentences
        if s.strip()
    ]


# ------------------------------------------------------------------
# SEMANTIC CHUNK CONSTRUCTION
# ------------------------------------------------------------------

def build_semantic_chunks(
    paragraphs: List[str],
    max_chars: int,
    overlap_sentences: int
) -> List[str]:
    """
    Build coherent semantic chunks.

    STRATEGY
    --------
    We accumulate sentences until:
    - chunk size exceeds max_chars

    Then:
    - finalize the chunk
    - preserve overlap sentences
    - continue building the next chunk

    WHY OVERLAP MATTERS
    -------------------
    Overlap preserves context continuity between chunks.

    This improves:
    - embeddings
    - semantic retrieval
    - final RAG answer quality
    """

    # Final chunk storage.
    chunks = []

    # Sentences currently being accumulated.
    current_chunk_sentences = []

    # Current chunk size tracker.
    current_chunk_length = 0

    # --------------------------------------------------------------
    # Process every paragraph.
    # --------------------------------------------------------------
    for paragraph in paragraphs:

        # Split paragraph into sentences.
        sentences = split_into_sentences(paragraph)

        # ----------------------------------------------------------
        # Process every sentence.
        # ----------------------------------------------------------
        for sentence in sentences:

            sentence_length = len(sentence)

            # ------------------------------------------------------
            # Determine if adding this sentence would exceed
            # the maximum chunk size.
            # ------------------------------------------------------
            exceeds_limit = (
                current_chunk_length + sentence_length > max_chars
            )

            # ------------------------------------------------------
            # If chunk limit exceeded:
            # finalize current chunk.
            # ------------------------------------------------------
            if exceeds_limit and current_chunk_sentences:

                chunk = finalize_chunk(
                    current_chunk_sentences
                )

                # Never store empty chunks.
                if chunk:
                    chunks.append(chunk)

                # --------------------------------------------------
                # Create semantic overlap.
                # --------------------------------------------------
                current_chunk_sentences = create_overlap(
                    current_chunk_sentences,
                    overlap_sentences
                )

                # Add current sentence to new chunk.
                current_chunk_sentences.append(sentence)

                # Recalculate chunk size.
                current_chunk_length = calculate_chunk_length(
                    current_chunk_sentences
                )

            else:
                # Continue accumulating semantic content.
                current_chunk_sentences.append(sentence)

                current_chunk_length += sentence_length

    # --------------------------------------------------------------
    # Add the final chunk.
    # --------------------------------------------------------------
    final_chunk = finalize_chunk(current_chunk_sentences)

    if final_chunk:
        chunks.append(final_chunk)

    return chunks


# ------------------------------------------------------------------
# CHUNK FINALIZATION
# ------------------------------------------------------------------

def finalize_chunk(sentences: List[str]) -> str:
    """
    Convert sentence list into a final chunk string.
    """

    return " ".join(sentences).strip()


# ------------------------------------------------------------------
# SEMANTIC OVERLAP
# ------------------------------------------------------------------

def create_overlap(
    sentences: List[str],
    overlap_sentences: int
) -> List[str]:
    """
    Create semantic overlap between chunks.

    IMPORTANT:
    We overlap FULL sentences instead of raw characters.

    WHY?
    ----
    Character overlap can:
    - cut words
    - break semantics
    - damage embeddings

    Sentence overlap preserves meaning.
    """

    if overlap_sentences <= 0:
        return []

    return sentences[-overlap_sentences:]


# ------------------------------------------------------------------
# CHUNK LENGTH CALCULATION
# ------------------------------------------------------------------

def calculate_chunk_length(sentences: List[str]) -> int:
    """
    Calculate total chunk character length.
    """

    return sum(len(s) for s in sentences)


# ------------------------------------------------------------------
# FINAL CLEANUP
# ------------------------------------------------------------------

def cleanup_chunks(chunks: List[str]) -> List[str]:
    """
    Final cleanup before embedding/storage.

    OPERATIONS
    ----------
    - normalize spaces
    - remove tiny/noisy chunks

    WHY REMOVE TINY CHUNKS?
    -----------------------
    Very small chunks often:
    - lack context
    - reduce retrieval quality
    - create noisy embeddings
    """

    cleaned = []

    for chunk in chunks:

        # Normalize whitespace.
        chunk = re.sub(r"\s+", " ", chunk).strip()

        # Skip tiny chunks.
        if len(chunk) > 80:
            cleaned.append(chunk)

    return cleaned