# rag/loader/chunker.py
# ------------------------------------------------------------
# PURPOSE:
#   Convert raw text into coherent, semantic chunks.
#
# WHY THIS MATTERS:
#   - RAG works best when chunks represent *meaningful units*
#     (paragraphs, sections), not random slices of text.
#   - Semantic chunking improves retrieval quality and reduces
#     hallucinations because the LLM sees complete ideas.
#
# STRATEGY:
#   1. Split text into paragraphs (semantic units)
#   2. Accumulate paragraphs until max_chars is reached
#   3. Start a new chunk when needed
#
# RESULT:
#   A list of coherent chunks, each containing 1–3 paragraphs.
# ------------------------------------------------------------

import re

def semantic_chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    """
    Split text into semantic chunks based on paragraphs.

    PARAMETERS
    ----------
    text : str
        The full raw text extracted from a document.

    max_chars : int
        Maximum number of characters allowed per chunk.
        This ensures chunks are not too large for embedding
        and remain efficient for retrieval.

    RETURNS
    -------
    list[str]
        A list of coherent text chunks.
    """

    # --------------------------------------------------------
    # 1. Split text into paragraphs.
    #
    # We split on double newlines because:
    #   - PDFs and books naturally separate paragraphs this way
    #   - It preserves semantic meaning
    #
    # We also strip whitespace and remove empty paragraphs.
    # --------------------------------------------------------
    paragraphs = [
        p.strip()
        for p in re.split(r"\n\s*\n", text)
        if p.strip()
    ]

    chunks = []      # Final list of chunks
    current = []     # Paragraphs being accumulated for current chunk
    total_chars = 0  # Character count of current chunk

    # --------------------------------------------------------
    # 2. Accumulate paragraphs until max_chars is reached.
    #
    # This ensures:
    #   - Chunks are coherent (multiple paragraphs)
    #   - No chunk exceeds the embedding model’s limits
    # --------------------------------------------------------
    for paragraph in paragraphs:
        paragraph_len = len(paragraph)

        # If adding this paragraph exceeds the limit → finalize chunk
        if total_chars + paragraph_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [paragraph]      # Start new chunk
            total_chars = paragraph_len
        else:
            current.append(paragraph)
            total_chars += paragraph_len

    # --------------------------------------------------------
    # 3. Add the last chunk if it contains any text.
    # --------------------------------------------------------
    if current:
        chunks.append("\n\n".join(current))

    return chunks
