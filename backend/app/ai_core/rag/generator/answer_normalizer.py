# rag/generator/answer_normalizer.py
# ------------------------------------------------------------
# PURPOSE:
#   Normalize the LLM final answer so it is:
#   - clean
#   - precise
#   - grounded
#   - without markdown
#   - without fluff
#   - without invented structure
# ------------------------------------------------------------

import re

def normalize_final_answer(text: str) -> str:
    """
    Normalize the LLM final answer:
    - remove markdown
    - remove headings
    - remove teacher tone
    - remove fluff
    - collapse multiple newlines
    - enforce clean paragraphs
    """

    # Remove markdown headings like **Title**, ### Title, etc.
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)
    text = re.sub(r"#+\s*", "", text)

    # Remove bold/italic markers
    text = text.replace("**", "").replace("*", "")

    # Remove "In summary", "To illustrate", "Welcome students", etc.
    text = re.sub(
        r"(In summary|To illustrate|Welcome.*?discussion|Fortunately|In conclusion).*?\.",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove "Additional Resources" or similar
    text = re.sub(r"Additional Resources.*", "", text, flags=re.IGNORECASE)

    # Collapse multiple newlines
    text = re.sub(r"\n{2,}", "\n", text)

    # Strip whitespace
    text = text.strip()

    return text
