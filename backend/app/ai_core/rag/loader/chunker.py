# rag/loader/chunker.py
# ------------------------------------------------------------------
# PRODUCTION-STYLE SEMANTIC CHUNKER FOR EDUCATIONAL RAG SYSTEMS
#
# Goals:
# - Preserve semantic meaning
# - Keep coherent explanations together
# - Avoid broken chunks
# - Improve embedding quality
# - Improve retrieval accuracy
# - Improve final LLM answers
#
# This chunker is designed especially for:
# - books
# - educational PDFs
# - research explanations
# - AI tutoring systems
# ------------------------------------------------------------------

import re
from typing import List


def semantic_chunk_text(
    text: str,
    max_chars: int = 1200,
    overlap_sentences: int = 2
) -> List[str]:
    """
    Create semantic chunks from normalized educational text.

    STRATEGY
    --------
    1. Preserve paragraph structure
    2. Split paragraphs into sentences
    3. Build coherent chunks
    4. Overlap using FULL sentences
       (not raw characters)

    WHY THIS IS BETTER
    ------------------
    Embeddings work best when chunks contain:
    - coherent ideas
    - meaningful explanations
    - related sentences

    NOT:
    - random character slices
    - broken words
    - isolated tiny fragments
    """

    # ------------------------------------------------------------------
    # 1. Normalize whitespace
    # ------------------------------------------------------------------
    # Convert repeated spaces/tabs into a single space.
    #
    # IMPORTANT:
    # We preserve newlines because they help maintain
    # semantic structure and paragraph boundaries.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive empty lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    # ------------------------------------------------------------------
    # 2. Split into paragraphs
    # ------------------------------------------------------------------
    # Paragraphs usually represent coherent ideas.
    #
    # This is MUCH better than forcing paragraph breaks
    # after every sentence.
    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    # Final chunks
    chunks = []

    # Current chunk state
    current_chunk_sentences = []
    current_chunk_length = 0

    # ------------------------------------------------------------------
    # 3. Process paragraphs
    # ------------------------------------------------------------------
    for paragraph in paragraphs:

        # --------------------------------------------------------------
        # Split paragraph into sentences
        # --------------------------------------------------------------
        #
        # Regex explanation:
        #
        # (?<=[.!?])
        #   split AFTER sentence punctuation
        #
        # \s+
        #   split on following spaces
        #
        sentences = re.split(
            r'(?<=[.!?])\s+',
            paragraph
        )

        # Remove empty sentences
        sentences = [
            s.strip()
            for s in sentences
            if s.strip()
        ]

        # --------------------------------------------------------------
        # 4. Build semantic chunks
        # --------------------------------------------------------------
        for sentence in sentences:

            sentence_length = len(sentence)

            # ----------------------------------------------------------
            # If adding this sentence exceeds chunk size:
            # finalize current chunk.
            # ----------------------------------------------------------
            if (
                current_chunk_length + sentence_length > max_chars
                and current_chunk_sentences
            ):

                # Join sentences into a single semantic chunk
                chunk = " ".join(current_chunk_sentences).strip()

                # Never store empty chunks
                if chunk:
                    chunks.append(chunk)

                # ------------------------------------------------------
                # OVERLAP STRATEGY
                # ------------------------------------------------------
                # Keep last N sentences from previous chunk.
                #
                # This helps preserve context between chunks.
                #
                # MUCH BETTER than raw character overlap.
                overlap = (
                    current_chunk_sentences[-overlap_sentences:]
                    if overlap_sentences > 0
                    else []
                )

                # Start next chunk with overlap + current sentence
                current_chunk_sentences = overlap + [sentence]

                # Recalculate chunk length
                current_chunk_length = sum(
                    len(s)
                    for s in current_chunk_sentences
                )

            else:
                # Continue accumulating semantic content
                current_chunk_sentences.append(sentence)
                current_chunk_length += sentence_length

    # ------------------------------------------------------------------
    # 5. Add final chunk
    # ------------------------------------------------------------------
    if current_chunk_sentences:

        chunk = " ".join(current_chunk_sentences).strip()

        if chunk:
            chunks.append(chunk)

    # ------------------------------------------------------------------
    # 6. Final safety cleanup
    # ------------------------------------------------------------------
    # Remove accidental duplicate spaces.
    cleaned_chunks = []

    for chunk in chunks:

        chunk = re.sub(r"\s+", " ", chunk).strip()

        # Skip tiny/noisy chunks
        if len(chunk) > 80:
            cleaned_chunks.append(chunk)

    return cleaned_chunks