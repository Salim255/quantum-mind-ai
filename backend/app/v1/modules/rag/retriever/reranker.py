from sentence_transformers import CrossEncoder
from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
# ------------------------------------------------------------
# CROSS-ENCODER RERANKER
# ------------------------------------------------------------
# This model is used AFTER vector search.
#
# It takes (query, document) pairs and directly predicts
# how relevant the document is to the query.
#
# Unlike embeddings (which are independent vectors),
# cross-encoders look at BOTH texts together.
#
# This makes them MUCH more accurate, but slower.
# ------------------------------------------------------------

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
# Controls batching size for inference safety.
# Large batches can cause:
# - memory spikes
# - GPU/CPU saturation
# ------------------------------------------------------------
BATCH_SIZE = 32


def rerank(query: str, docs: List[RetrievalChunkDTO]) ->  List[RetrievalChunkDTO]:
    """
    Re-ranks retrieved documents using a cross-encoder model.

    This step improves precision by re-evaluating
    semantic relevance between query and documents.

    Parameters
    ----------
    query : str
        User question.

    docs : List[RetrievalChunkDTO]
        Candidate chunks from vector search.

    Returns
    -------
    List[RetrievalChunkDTO]
        Same objects enriched with rerank_score,
        sorted by final relevance.
    """

    # ------------------------------------------------------------
    # 1. BUILD QUERY-DOCUMENT PAIRS
    # ------------------------------------------------------------
    # We convert retrieval candidates into model input format.
    # Each pair is independently scored by the cross-encoder.
    # ------------------------------------------------------------
    pairs = [(query, doc.text) for doc in docs]
  

    # ------------------------------------------------------------
    # 2. BATCHED PREDICTION
    # ------------------------------------------------------------
    # We avoid sending all pairs at once to prevent:
    # - memory overload
    # - inference instability
    # ------------------------------------------------------------
    all_scores: List[float] = []

    for i in range(0, len(pairs), BATCH_SIZE):
        batch = pairs[i:i + BATCH_SIZE]

        batch_scores = reranker.predict(batch)

        # Ensure consistent Python list type
        all_scores.extend(list(batch_scores))


    # ------------------------------------------------------------
    # 3. ATTACH SCORES TO DTOs (NO STRUCTURE CHANGE)
    # ------------------------------------------------------------
    # We mutate only score fields, not structure.
    # This keeps pipeline compatible with later stages.
    # ------------------------------------------------------------
    for doc, score in zip(docs, all_scores):
        doc.rerank_score = float(score)

    # ------------------------------------------------------------
    # 4. COMPUTE HYBRID SCORE (FINAL SCORING LAYER)
    # ------------------------------------------------------------
    # Hybrid scoring balances:
    # - reranker precision (semantic understanding)
    # - cosine recall safety (embedding similarity)
    # ------------------------------------------------------------
    for doc in docs:
        doc.hybrid_score = (
            0.7 * (doc.rerank_score or 0.0) +
            0.3 * (doc.cosine_score or 0.0)
        )

     # ------------------------------------------------------------
    # 5. FINAL SORTING (PRIMARY SIGNAL = RERANK SCORE)
    # ------------------------------------------------------------
    docs.sort(key=lambda x: x.rerank_score or 0.0, reverse=True)
    
    return docs
