import re
# re = Python regular expressions module.
# Used here to repair common PDF extraction problems.


def normalize_text(text: str) -> str:
    """
    Normalize PDF text structure before semantic chunking.

    WHY THIS STEP EXISTS
    --------------------
    Raw PDF extraction is usually messy.

    Common problems:
    - words split across lines
    - broken sentences
    - random line breaks
    - inconsistent spacing
    - damaged paragraph structure

    This function repairs the text so chunking becomes
    much more semantically accurate.

    IMPORTANT:
    Good normalization improves:
    - chunk quality
    - embedding quality
    - retrieval quality
    - final RAG answers
    """

    # -------------------------------------------------------------------------
    # 1. Fix hyphenated line breaks
    # -------------------------------------------------------------------------
    # PDFs often split words across lines:
    #
    #   inter-
    #   action
    #
    # becomes:
    #
    #   interaction
    #
    # Explanation:
    # -\s*\n\s*
    #
    # - matches "-"
    # - optional spaces
    # - newline
    # - optional spaces after newline
    text = re.sub(
        r"-\s*\n\s*",
        "",
        text
    )

    # -------------------------------------------------------------------------
    # 2. Normalize excessive newlines
    # -------------------------------------------------------------------------
    # Converts:
    #
    #   \n\n\n\n
    #
    # into:
    #
    #   \n
    #
    # This reduces noisy spacing from PDF extraction.
    text = re.sub(
        r"\n{2,}",
        "\n",
        text
    )

    # -------------------------------------------------------------------------
    # 3. Repair sentences broken across lines
    # -------------------------------------------------------------------------
    # PDFs often contain:
    #
    #   Quantum computing is
    #   a fascinating field.
    #
    # We convert this into:
    #
    #   Quantum computing is a fascinating field.
    #
    # Explanation:
    #
    # (?<![.!?])
    #   previous character is NOT punctuation
    #
    # \n
    #   newline
    #
    # (?!\n)
    #   next character is NOT another newline
    #
    # Meaning:
    # replace "soft line breaks" inside sentences with spaces.
    text = re.sub(
        r"(?<![.!?])\n(?!\n)",
        " ",
        text
    )

    # -------------------------------------------------------------------------
    # 4. Create clearer sentence boundaries
    # -------------------------------------------------------------------------
    # Converts:
    #
    #   Sentence one. Sentence two.
    #
    # into:
    #
    #   Sentence one.
    #   Sentence two.
    #
    # This helps semantic chunking identify logical boundaries.
    #
    # ([.!?])
    # captures sentence-ending punctuation.
    #
    # \s+
    # matches following spaces.
    #
    # r"\1\n"
    # reinserts punctuation + newline.
    text = re.sub(
        r"([.!?])\s+",
        r"\1\n",
        text
    )

    # -------------------------------------------------------------------------
    # 5. Normalize spaces and tabs
    # -------------------------------------------------------------------------
    # Converts:
    #
    #   "hello      world"
    #
    # into:
    #
    #   "hello world"
    #
    # IMPORTANT:
    # We do NOT remove newlines here.
    # Newlines help preserve semantic structure.
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # -------------------------------------------------------------------------
    # 6. Final cleanup
    # -------------------------------------------------------------------------
    # strip() removes leading/trailing whitespace.
    return text.strip()