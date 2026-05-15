import re

def normalize_text(text: str) -> str:
    """
    Normalize PDF text structure:
    - fix hyphenated line breaks
    - fix mid-sentence newlines
    - enforce paragraph boundaries
    - clean spacing
    """

    # Remove hyphenation at line breaks: "inter-\naction" → "interaction"
    text = re.sub(r"-\s*\n\s*", "", text)

    # Replace multiple newlines with a single newline
    text = re.sub(r"\n{2,}", "\n", text)

    # Replace single newlines inside sentences with spaces
    text = re.sub(r"(?<![.!?])\n(?!\n)", " ", text)

    # Ensure sentences end with a newline → paragraph detection
    text = re.sub(r"([.!?])\s+", r"\1\n", text)

    # Remove extra spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()
