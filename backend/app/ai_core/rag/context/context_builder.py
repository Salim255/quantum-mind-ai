# rag/context/context_builder.py

def build_context(chunks: list[str], max_chars: int = 3000) -> list[str]:
    """
    Build a richer context by taking as many top chunks as possible
    without exceeding max_chars in total length.
    Returns a list with 1 merged context string.
    """

    merged = []
    total = 0

    for chunk in chunks:
        length = len(chunk)
        if total + length > max_chars:
            break
        merged.append(chunk)
        total += length

    # We return a list[str] because RAGPromptBuilder expects a list of chunks.
    # Here it's effectively a single, richer chunk.
    return ["\n\n".join(merged)]
