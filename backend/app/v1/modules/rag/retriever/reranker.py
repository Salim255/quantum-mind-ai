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


def rerank(query: str, docs: List[RetrievalChunkDTO]) ->  List[RetrievalChunkDTO]:
    """
    Re-ranks candidate documents using a cross-encoder model.

    PARAMETERS
    ----------
    query : str
        The user question (e.g., "what is quantum entanglement?")

    docs : List[Dict[str, Any]]
        Candidate chunks from vector search.
        Each doc must contain:
            - text (str)
            - cosine_score (float, optional)

    RETURNS
    -------
    List[Dict[str, Any]]
        Same docs enriched with:
            - rerank_score (float)
        Sorted from most relevant → least relevant
    """

    # ------------------------------------------------------------
    # 1. Build query-document pairs
    # ------------------------------------------------------------
    pairs = [(query, d.text) for d in docs]

    # ------------------------------------------------------------
    # 2. Predict relevance scores
    # ------------------------------------------------------------
    scores: List[float] = reranker.predict(pairs)
    scores = list(scores)

    # Attach scores
    # ------------------------------------------------------------
    # 3. Attach rerank scores back to documents
    # ------------------------------------------------------------
    for doc, score in zip(docs, scores):
        doc.rerank_score = float(score)


    # ------------------------------------------------------------
    # 4. compute hybrid score (same pass, still safe)
    # ------------------------------------------------------------
    # We combine:
    # - reranker score (semantic precision)
    # - cosine score (embedding recall safety net)
    #
    # This prevents losing high-similarity chunks.
    # ------------------------------------------------------------
    for doc in docs:
        doc.hybrid_score = (
            0.7 * (doc.rerank_score or 0.0) +
            0.3 * (doc.cosine_score or 0.0)
        )

    return docs
