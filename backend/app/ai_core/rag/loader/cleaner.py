import re

def clean_text(text: str) -> str:
    """
    Clean PDF text by removing equations, LaTeX, symbols, and noise.
    """

    # Remove LaTeX math blocks: $...$ or $$...$$
    text = re.sub(r'\${1,2}.*?\${1,2}', ' ', text, flags=re.DOTALL)

    # Remove inline equations like (1.2), [3], etc.
    text = re.sub(r'\(\d+(\.\d+)?\)', ' ', text)
    text = re.sub(r'\[\d+\]', ' ', text)

    # Remove unicode math symbols
    text = re.sub(r'[⟨⟩⊗∑ψαβγλμνΩωσρπθ]', ' ', text)

    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()
