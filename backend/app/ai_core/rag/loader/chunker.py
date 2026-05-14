# rag/loader/chunker.py

def chunk_text(text: str, chunk_size: int = 500):
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

    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)

        # If the chunk is too big, finalize it.
        if len(" ".join(current)) > chunk_size:
            chunks.append(" ".join(current))
            current = []

    # Add the last chunk if not empty.
    if current:
        chunks.append(" ".join(current))

    return chunks
