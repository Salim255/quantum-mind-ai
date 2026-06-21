# rag/generator/answer_normalizer.py
# ------------------------------------------------------------
# PURPOSE:
#   Clean ONLY formatting artifacts from the LLM output.
#   It must NOT change meaning, structure, or content.
# ------------------------------------------------------------

import re

def normalize_final_answer(text: str) -> str:
    """
    Clean LLM output for UI rendering.

    RESPONSIBILITY:
    - Fix escaped newlines
    - Remove excessive spacing
    - Ensure clean readable paragraphs

    DO NOT:
    - rewrite content
    - remove ideas
    - alter meaning
    """

    if not text:
        return ""

    # ------------------------------------------------------------
    # 1. Fix escaped newlines (IMPORTANT)
    # ------------------------------------------------------------
    text = text.replace("\\n", "\n")

    # ------------------------------------------------------------
    # 2. Normalize excessive newlines
    # ------------------------------------------------------------
    text = re.sub(r"\n{3,}", "\n\n", text)

    # ------------------------------------------------------------
    # 3. Clean trailing/leading spaces per line
    # ------------------------------------------------------------
    text = "\n".join(line.strip() for line in text.split("\n"))

    # ------------------------------------------------------------
    # 4. Final cleanup
    # ------------------------------------------------------------
    return text.strip()