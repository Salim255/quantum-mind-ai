import numpy as np

from app.ai_core.rag.embeddings.embedder import embed_text
from app.ai_core.rag.vector_store.store import VECTOR_DB
from app.ai_core.rag.retriever.reranker import rerank


def search_similar_documents(query: str, top_k: int = 3):
    """
    HYBRID SEMANTIC RETRIEVAL PIPELINE

    This function performs high-quality retrieval using:
    1. Dense embeddings (cosine similarity) → recall layer
    2. Cross-encoder reranker → precision layer
    3. Hybrid scoring → prevents losing strong matches

    WHY THIS DESIGN IS IMPORTANT
    ----------------------------
    - Cosine similarity ensures recall (finds relevant candidates)
    - Reranker ensures precision (reorders best answers)
    - Hybrid scoring prevents losing high-similarity matches
    """

    # ------------------------------------------------------------
    # 1. Embed query into vector space
    # ------------------------------------------------------------
    q_emb = np.array(
        embed_text(text=query, source="user_query")["embedding"]
    )

    scored = []

    print(f"[SEARCH] VECTOR_DB size: {len(VECTOR_DB)}")

    # ------------------------------------------------------------
    # 2. Compute cosine similarity against all documents
    # ------------------------------------------------------------
    for doc in VECTOR_DB:

        d_emb = np.array(doc["embedding"])

        # cosine similarity (vector alignment)
        cosine_score = np.dot(q_emb, d_emb) / (
            np.linalg.norm(q_emb) * np.linalg.norm(d_emb)
        )

        scored.append({
            "text": doc["text"],
            "source": doc["source"],
            "cosine_score": float(cosine_score)  # IMPORTANT: keep this
        })

    # ------------------------------------------------------------
    # 3. Sort by cosine similarity (recall stage)
    # ------------------------------------------------------------
    scored.sort(key=lambda x: x["cosine_score"], reverse=True)

    # ------------------------------------------------------------
    # 4. Expand candidate pool (IMPORTANT FIX)
    # ------------------------------------------------------------
    # We take more than top_k to avoid losing strong matches
    top_candidates = scored[:30]

    print(f"[SEARCH] candidates sent to reranker: {len(top_candidates)}")

    # ------------------------------------------------------------
    # 5. Rerank using cross-encoder (precision stage)
    # ------------------------------------------------------------
    reranked = rerank(query, top_candidates)

    # ------------------------------------------------------------
    # 6. Hybrid scoring (CRITICAL FIX)
    # ------------------------------------------------------------
    # We combine:
    # - reranker score (semantic precision)
    # - cosine score (embedding recall safety net)
    #
    # This prevents losing high-similarity chunks.
    # ------------------------------------------------------------
    for item in reranked:
        item["hybrid_score"] = (
            0.7 * item.get("rerank_score", 0) +
            0.3 * item.get("cosine_score", 0)
        )

    # ------------------------------------------------------------
    # 7. Final ranking based on hybrid score
    # ------------------------------------------------------------
    reranked.sort(key=lambda x: x["hybrid_score"], reverse=True)

    # ------------------------------------------------------------
    # 8. Return top-k results
    # ------------------------------------------------------------
    return {
        "results": [d["text"] for d in reranked[:top_k]],
        "sources": [d["source"] for d in reranked[:top_k]]
    }