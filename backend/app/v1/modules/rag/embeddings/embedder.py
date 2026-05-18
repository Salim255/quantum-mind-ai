"""
Embedding module for the RAG system.

This file provides a clean, production‑grade interface for generating
dense vector embeddings from text. These embeddings are the foundation
of semantic search and retrieval.
"""

# Import the SentenceTransformer model used for generating embeddings.
# This model converts text into high‑dimensional vectors that capture meaning.
from sentence_transformers import SentenceTransformer

# NumPy is used later in the pipeline for similarity calculations.
import numpy as np


# Load the embedding model ONCE at module import time.
# This avoids reloading the model on every request, which would be slow.
# "all-MiniLM-L6-v2" is a fast, lightweight, high‑quality embedding model.
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_text(text: str, source: str = "document") -> dict:
    """
    Convert a text string into a dense embedding vector.

    Parameters
    ----------
    text : str
        The input text to embed.

    Returns
    -------
    dict
        A dictionary containing the embedding under the key "embedding".
        The embedding is returned as a Python list (not a NumPy array)
        so it can be serialized to JSON and passed through your tool‑calling system.
    """

    # Encode the text into a dense vector using the loaded model.
    # The output is a NumPy array, which we convert to a list for JSON compatibility.
    embedding = model.encode(text).tolist()

    # Return the embedding wrapped in a dict.
    return {"embedding": embedding, "source": source}