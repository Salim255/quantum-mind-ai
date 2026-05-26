import re


def clean_text(text: str) -> str:
    """
    SAFE RAG TEXT CLEANER
    =====================

    Goal:
    -----
    Clean PDF/OCR text WITHOUT destroying meaning.

    Principle:
    ----------
    - Preserve semantic content
    - Preserve structure (paragraphs, headings)
    - Only remove obvious noise

    This is optimized for:
    - embeddings quality
    - retrieval accuracy
    - hybrid search compatibility
    """

    # ------------------------------------------------------------
    # 1. Normalize encoding issues
    # ------------------------------------------------------------
    # WHY:
    # PDFs often contain weird unicode artifacts:
    # - broken spaces
    # - invisible characters
    # - inconsistent encoding
    #
    # We normalize early to avoid embedding noise.
    text = text.replace("\x00", " ")

    # ------------------------------------------------------------
    # 2. Remove LaTeX math blocks (SAFE VERSION)
    # ------------------------------------------------------------
    # WHY:
    # Math blocks often add noise for semantic search
    # BUT: we remove only clearly bounded expressions
    #
    # SAFETY:
    # This avoids removing large accidental chunks.
    text = re.sub(r'\${1,2}[^$]{1,2000}?\${1,2}', ' ', text)

    # ------------------------------------------------------------
    # 3. Remove citation markers [1], [23]
    # ------------------------------------------------------------
    # WHY:
    # Citations rarely help embeddings
    text = re.sub(r'\[\d{1,4}\]', ' ', text)

    # ------------------------------------------------------------
    # 4. Fix hyphenated line breaks (VERY IMPORTANT)
    # ------------------------------------------------------------
    # WHY:
    # PDFs often break words like:
    #   "transfor-"
    #   "mation"
    #
    # We reconstruct proper words.
    text = re.sub(r'-\n\s*', '', text)

    # ------------------------------------------------------------
    # 5. Remove repeated single page numbers ONLY
    # ------------------------------------------------------------
    # WHY:
    # Safe removal of isolated page numbers
    #
    # IMPORTANT:
    # Only removes standalone numeric lines.
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)

    # ------------------------------------------------------------
    # 6. Remove obvious copyright / publisher noise
    # ------------------------------------------------------------
    # WHY:
    # These sections do not contribute semantic value
    noise_patterns = [
        r'all rights reserved',
        r'copyright',
        r'isbn',
        r'lccn',
        r'library of congress',
        r'cataloging[-\s]in[-\s]publication',
        r'printed and bound',
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)

    # ------------------------------------------------------------
    # 7. DO NOT REMOVE CHAPTERS OR HEADINGS
    # ------------------------------------------------------------
    # WHY:
    # These are IMPORTANT for chunking + retrieval.
    #
    # ❌ Removed:
    #   chapter removal regex
    #   "introduction" removal
    #   TOC structure removal
    #
    # Reason:
    # They are semantic anchors.

    # ------------------------------------------------------------
    # 8. Normalize spaces (SAFE VERSION)
    # ------------------------------------------------------------
    # WHY:
    # We reduce noise but preserve structure.
    text = re.sub(r'[ \t]+', ' ', text)

    # ------------------------------------------------------------
    # 9. Normalize excessive newlines
    # ------------------------------------------------------------
    # WHY:
    # Keeps paragraph structure intact
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ------------------------------------------------------------
    # 10. Final trim
    # ------------------------------------------------------------
    return text.strip()