import re


def clean_text(text: str) -> str:
    """
    CLEAN TEXT FOR RAG PIPELINE (FINAL PRODUCTION VERSION)
    =====================================================

    PURPOSE
    -------
    Remove ONLY extraction noise from PDF text while preserving meaning.

    PRINCIPLE
    ---------
    - DO NOT rewrite sentences
    - DO NOT infer structure
    - DO NOT improve readability
    - ONLY fix corruption from PDF extraction

    WHY THIS IS IMPORTANT
    ---------------------
    Bad cleaning = lost keywords + bad retrieval
    Good cleaning = stable embeddings + correct RAG results
    """

    # ------------------------------------------------------------
    # 1. REMOVE MATH / INLINE FORMULAS (NOISE FOR RAG)
    # ------------------------------------------------------------
    # WHY:
    # Math expressions rarely help semantic search and add noise
    text = re.sub(r'\${1,2}[^$]{1,2000}?\${1,2}', ' ', text)

    # ------------------------------------------------------------
    # 2. REMOVE CITATIONS LIKE [1], [23]
    # ------------------------------------------------------------
    # WHY:
    # Citations are metadata, not semantic content
    text = re.sub(r'\[\d{1,4}\]', ' ', text)

    # ------------------------------------------------------------
    # 3. FIX HYPHENATED LINE BREAKS (CRITICAL STEP)
    # ------------------------------------------------------------
    # WHY THIS EXISTS:
    # PDFs split words at line breaks:
    #
    #   inter-
    #   action
    #
    # WITHOUT FIX:
    # - embeddings break words
    # - keyword search fails
    #
    # WITH FIX:
    # - restores original word integrity
    text = re.sub(r"-\s*\n\s*", "", text)

    # ------------------------------------------------------------
    # 4. REMOVE ISOLATED PAGE NUMBERS
    # ------------------------------------------------------------
    # WHY:
    # Page numbers have no semantic meaning
    text = re.sub(r'^\s*\d{1,4}\s*$', '', text, flags=re.MULTILINE)

    # ------------------------------------------------------------
    # 5. REMOVE COMMON PDF BOILERPLATE NOISE
    # ------------------------------------------------------------
    # WHY:
    # These are repeated publisher artifacts that pollute embeddings
    noise_patterns = [
        r'all rights reserved',
        r'copyright',
        r'isbn',
        r'lccn',
        r'library of congress',
    ]

    for pattern in noise_patterns:
        text = re.sub(pattern, ' ', text, flags=re.IGNORECASE)

    # ------------------------------------------------------------
    # 6. NORMALIZE SPACES (STRUCTURAL STABILIZATION)
    # ------------------------------------------------------------
    # WHY THIS COMES LATE:
    # After removing noise, spacing becomes inconsistent
    #
    # WHAT IT DOES:
    # "word     word" → "word word"
    #
    # IMPACT IF REMOVED:
    # - unstable tokenization
    # - noisy embeddings
    text = re.sub(r"[ \t]+", " ", text)

    # ------------------------------------------------------------
    # 7. NORMALIZE EXCESS NEWLINES
    # ------------------------------------------------------------
    # WHY:
    # Prevents excessive blank gaps from PDF extraction
    text = re.sub(r'\n{3,}', '\n\n', text)

    # ------------------------------------------------------------
    # 8. FINAL CLEANUP
    # ------------------------------------------------------------
    # WHY:
    # Ensures consistent output formatting for chunking stage
    return text.strip()