# rag/loader/chunker.py
# ------------------------------------------------------------
# Robust semantic chunker that:
# 1. Normalizes PDF text
# 2. Creates paragraphs even if PDF has no blank lines
# 3. Splits into semantic chunks
# 4. Adds overlap
# 5. Never returns empty chunks
# ------------------------------------------------------------

import re
from typing import List

def semantic_chunk_text(
    text: str,
    max_chars: int = 1200,
    overlap_chars: int = 200
) -> List[str]:
    """
    Robust semantic chunking for messy PDF text.

    Steps:
    - Normalize line breaks
    - Create paragraphs even when PDF has no blank lines
    - Accumulate paragraphs into chunks
    - Add overlap between chunks
    """

    # --------------------------------------------------------
    # 1. Normalize PDF text
    # --------------------------------------------------------

    # Replace multiple spaces/newlines with a single space
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", "\n", text)

    # Force paragraph breaks after periods if needed
    # This handles PDFs with no blank lines
    text = re.sub(r"\.\s+", ".\n", text)

    # --------------------------------------------------------
    # 2. Split into paragraphs
    # --------------------------------------------------------
    paragraphs = [
        p.strip()
        for p in text.split("\n")
        if p.strip()
    ]

    chunks = []
    current = []
    current_len = 0

    # --------------------------------------------------------
    # 3. Build semantic chunks
    # --------------------------------------------------------
    for p in paragraphs:
        p_len = len(p)

        if current_len + p_len > max_chars and current:
            chunk = "\n\n".join(current).strip()
            if chunk:
                chunks.append(chunk)

            # Overlap tail
            tail = chunk[-overlap_chars:] if overlap_chars > 0 else ""
            current = [tail, p] if tail else [p]
            current_len = len(tail) + p_len
        else:
            current.append(p)
            current_len += p_len

    # Last chunk
    if current:
        chunk = "\n\n".join(current).strip()
        if chunk:
            chunks.append(chunk)

    return chunks
