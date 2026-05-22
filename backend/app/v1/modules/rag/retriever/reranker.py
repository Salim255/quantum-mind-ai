from sentence_transformers import CrossEncoder
from typing import List
from app.v1.modules.rag.dto.rerank_dto import RerankDocumentDTO, RerankResponseDTO
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


def rerank(query: str, docs: List[RerankDocumentDTO]) ->  RerankResponseDTO:
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

    # Sort by rerank score
    # ------------------------------------------------------------
    # 4. Sort by rerank score (primary ranking signal)
    # ------------------------------------------------------------
    docs.sort(key=lambda x: x.rerank_score, reverse=True)

    return docs
