import numpy as np
# NumPy is used for handling vectors (embeddings).
# Even if this function does not manipulate vectors directly,
# NumPy is essential for similarity search later in the pipeline.

from rag.embeddings.embedder import embed_text
# Import the embedding function.
# This function converts raw text into a dense vector representation
# that your QuantumMind AI system will use for retrieval.


# In-memory vector database.
# Each entry will look like:
# { "text": "...", "embedding": [0.12, -0.44, ...], "source": "lesson" }
VECTOR_DB = []


def add_document(text: str, source: str = "lesson"):
    """
    Add a document to the QuantumMind AI vector store.

    Parameters
    ----------
    text : str
        The raw text content to store and embed.
        This can be a lesson, explanation, formula description,
        or any quantum learning material.

    source : str
        A tag describing the origin of the content.
        Helps the retriever prioritize and rank results.
        Defaults to "lesson".

    Returns
    -------
    dict
        A simple status dictionary confirming the operation.
    """

    # --- 1. Generate an embedding for the provided text ----------------------
    # The embed_text() tool returns a dictionary:
    # { "embedding": [...], "normalize": True, "source": "lesson" }
    # We extract only the vector because that's what we store in the DB.
    embedding_result = embed_text(text=text, source=source)
    emb = embedding_result["embedding"]


    # --- 2. Build the document entry ----------------------------------------
    # We store:
    # - the raw text (for retrieval context)
    # - the embedding vector (for similarity search)
    # - the source tag (for smarter ranking)
    document_entry = {
        "text": text,
        "embedding": emb,
        "source": source
    }


    # --- 3. Save the entry in the in-memory vector DB -----------------------
    # This is your temporary vector store.
    # Later you can replace this with:
    # - a persistent DB (PostgreSQL + pgvector)
    # - a cloud vector DB (Pinecone, Weaviate, Qdrant)
    VECTOR_DB.append(document_entry)


    # --- 4. Return a confirmation -------------------------------------------
    # The agent_core expects a JSON-serializable response.
    return {
        "status": "ok",
        "stored_text_length": len(text),
        "source": source
    }
