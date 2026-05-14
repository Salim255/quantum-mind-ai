import numpy as np
# NumPy is used for vector math: dot products, norms, cosine similarity.
# It is the backbone of semantic search operations.

from app.ai_core.rag.embeddings.embedder import embed_text
# This is your embedding tool.
# It converts raw text (queries, lessons, formulas, etc.) into dense vectors.

from app.ai_core.rag.vector_store.store import VECTOR_DB
# This is your in-memory vector store.
# Each entry looks like:
# { "text": "...", "embedding": [...], "source": "lesson" }


def search_similar_documents(query: str, top_k: int = 3):
    """
    Perform semantic search over the QuantumMind AI vector store.

    Parameters
    ----------
    query : str
        The user question or text to embed and compare against stored content.

    top_k : int
        Number of top results to return (default: 3).

    Returns
    -------
    dict
        A dictionary containing the list of retrieved texts.
    """

    # --- 1. Convert the query into an embedding vector -----------------------
    # embed_text() returns a dictionary:
    # { "embedding": [...], "source": "user_query", ... }
    # We extract only the embedding vector.
    q_emb = np.array(embed_text(text=query, source="user_query")["embedding"])

    #print(f"Query embedding generated: {q_emb}...")  # Debug log to confirm embedding generation (first 5 dimensions) --- IGNORE ---
    # --- 2. Prepare a list to store similarity scores ------------------------
    # Each entry will be a tuple: (similarity_score, document_text)
    # Example: (0.87, "The Hadamard gate creates superposition...")
    scored = []

    print(f"Starting semantic search for query: '{len(VECTOR_DB)}'...")  # Debug log to confirm search start --- IGNORE ---
    # --- 3. Iterate over every stored document in the vector DB --------------
    for doc in VECTOR_DB:

        # Convert the stored embedding to a NumPy array for math operations.
        d_emb = np.array(doc["embedding"])
        print(f"Comparing with document: {doc}...")  # Debug log to confirm document being compared (first 50 chars) --- IGNORE ---    
        # --- 4. Compute cosine similarity ------------------------------------
        # Cosine similarity formula:
        # score = (q ⋅ d) / (||q|| * ||d||)
        #
        # - q ⋅ d  → dot product (measures alignment)
        # - ||q||  → magnitude of query vector
        # - ||d||  → magnitude of document vector
        #
        # Result is between:
        # -1 → opposite meaning
        #  0 → unrelated
        # +1 → identical meaning
        score = np.dot(q_emb, d_emb) / (np.linalg.norm(q_emb) * np.linalg.norm(d_emb))

        # Store the score and the document text.
        scored.append((score, doc["text"]))


    # --- 5. Sort results by similarity score (highest first) -----------------
    scored.sort(reverse=True, key=lambda x: x[0])


    # --- 6. Extract only the text of the top_k results -----------------------
    top_results = [text for _, text in scored[:top_k]]

    print(f"Top {top_k} results: {top_results}")  # Debug log to confirm retrieved results --- IGNORE ---
    # Return results in a JSON-friendly structure.
    return {"results": top_results}
