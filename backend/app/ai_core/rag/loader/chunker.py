# rag/loader/chunker.py
import re

def chunk_text(text: str, chunk_size: int = 400, overlap: int = 50):
    """
    Split long text into smaller chunks for better retrieval.

    Parameters
    ----------
    text : str
        The full text to split.

    chunk_size : int
        Maximum number of characters per chunk.

    Returns
    -------
    list[str]
        List of text chunks.
    """

    sentences  = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current = ""

    for sentence in sentences:
         # If adding this sentence exceeds chunk size → finalize chunk
        if len(current) + len(sentence) > chunk_size:
            chunks.append(current.strip())
            # Start new chunk with overlap
            current = current[-overlap:] + " " + sentence
        else:
            current += " " + sentence

    # Add last chunk
    if current.strip():
        chunks.append(current.strip())

    return chunks
