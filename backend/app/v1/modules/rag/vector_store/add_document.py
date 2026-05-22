import numpy as np
# NumPy is used for handling vectors (embeddings).
# Even if this function does not manipulate vectors directly,
# NumPy is essential for similarity search later in the pipeline.
from app.v1.modules.rag.vector_store.store import VECTOR_DB
from app.v1.modules.rag.embeddings.embedder import embed_text
from app.v1.modules.rag.dto.chunk_dto import ChunkDTO
from app.v1.modules.rag.dto.document_dto import DocumentDTO, AddedDocResponseDto
# Import the embedding function.
# This function converts raw text into a dense vector representation
# that your QuantumMind AI system will use for retrieval.


# In-memory vector database.
# Each entry will look like:
# { "text": "...", "embedding": [0.12, -0.44, ...], "source": "lesson" }


def add_document(chunk: ChunkDTO, source: str = "document") -> AddedDocResponseDto:
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
        Defaults to "document".

    Returns
    -------
    dict
        A simple status dictionary confirming the operation.
    """

    # --- 1. Generate an embedding for the provided text ----------------------
    # The embed_text() tool returns a dictionary:
    # { "embedding": [...], "normalize": True, "source": "lesson" }
    # We extract only the vector because that's what we store in the DB.
    # 1. Extract text safely
    # text = chunk["text"] if isinstance(chunk, dict) else chunk
    text = chunk["text"]
    embedding_result = embed_text(text=text, source=source)
    emb = embedding_result["embedding"]


    # --- 2. Build the document entry ----------------------------------------
    # We store:
    # - the raw text (for retrieval context)
    # - the embedding vector (for similarity search)
    # - the source tag (for smarter ranking)
    concept = chunk.get("concept", "unknown") if isinstance(chunk, ChunkDTO) else "unknown"
    
    document_entry = DocumentDTO(
        text,
        emb,
        source,
        concept
        )


    # --- 3. Save the entry in the in-memory vector DB -----------------------
    # This is your temporary vector store.
    # Later you can replace this with:
    # - a persistent DB (PostgreSQL + pgvector)
    # - a cloud vector DB (Pinecone, Weaviate, Qdrant)
    VECTOR_DB.append(document_entry)

    # --- 4. Return a confirmation -------------------------------------------
    # The agent_core expects a JSON-serializable response.
    return AddedDocResponseDto(
            status="ok",
            stored_text_length=len(text),
            source=source
        )