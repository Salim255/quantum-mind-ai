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

from app.ai_core.rag.retriever.reranker import rerank
# This is your cross-encoder reranker.
# It reads (query, chunk) pairs and scores true semantic relevance.
# This dramatically improves retrieval accuracy.


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

    # --- 2. Prepare a list to store similarity scores ------------------------
    # Each entry will be a dictionary:
    # {
    #     "score": cosine_similarity_value,
    #     "text": "...",
    #     "source": "document"
    # }
    scored = []

    print(f"Starting semantic search. VECTOR_DB contains {len(VECTOR_DB)} documents...")

    # --- 3. Iterate over every stored document in the vector DB --------------
    for doc in VECTOR_DB:

        # Convert the stored embedding to a NumPy array for math operations.
        d_emb = np.array(doc["embedding"])

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

        # Store the score and the document text in a dictionary (NOT a tuple).
        scored.append({
            "score": float(score),
            "text": doc["text"],
            "source": doc["source"]
        })

    # --- 5. Sort results by cosine similarity (highest first) ----------------
    scored.sort(key=lambda x: x["score"], reverse=True)

    # Take the top 10 candidates for reranking
    top_candidates = scored[:10]

    print(f"Top raw cosine candidates: {len(top_candidates)}")

    # --- 6. Rerank using the cross-encoder -----------------------------------
    # The reranker reads (query, chunk) pairs and assigns a relevance score.
    # This step dramatically improves accuracy.
    reranked = rerank(query, top_candidates)

    print(f"Top reranked results: {reranked[:top_k]}")

    # --- 7. Return only the text of the top_k results -------------------------
    return {"results": [d["text"] for d in reranked[:top_k]], "sources": [d["source"] for d in reranked[:top_k]]}
