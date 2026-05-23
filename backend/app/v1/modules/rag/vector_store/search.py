import numpy as np
from typing import List

from app.v1.modules.rag.embeddings.embedder import embed_text
from app.v1.modules.rag.vector_store.store import VECTOR_DB
from app.v1.modules.rag.retriever.reranker import rerank
from app.v1.modules.rag.retriever.query_expander import expand_query
from app.v1.modules.rag.retriever.decision_engine import decide_retrieval_action
from app.v1.modules.rag.dto.retrieval_dto import (
    RetrievalResponseDTO,
    RetrievalChunkDTO
)
from app.v1.modules.rag.retriever.decision_engine import RetrievalAction
from app.v1.modules.rag.retriever.diversity_filter import diversify_results

# ============================================================
# RETRIEVAL THRESHOLDS
# ============================================================
#
# MIN_SIMILARITY_SCORE
# --------------------
# Minimum cosine similarity required for a chunk
# to enter the reranking stage.
#
# WHY IMPORTANT?
# --------------
# Prevents obviously irrelevant chunks from:
# - wasting reranker computation
# - polluting context
# - increasing hallucinations
#
# Example:
# A chunk about "classical mechanics"
# should never be retrieved for:
# "what is quantum entanglement?"
# ============================================================

MIN_SIMILARITY_SCORE = 0.25


# ============================================================
# MIN_CONFIDENCE_SCORE
# ============================================================
#
# Minimum final hybrid score required before
# the system trusts retrieval enough to answer.
#
# WHY IMPORTANT?
# --------------
# Even after reranking:
# - some queries may still have weak matches
# - weak context produces hallucinations
#
# If confidence is too low:
# → system returns NO CONTEXT
# → generator can safely say:
#   "I don't have enough information."
# ============================================================

MIN_CONFIDENCE_SCORE = 1.5


def search_similar_documents(
    query: str,
    top_k: int = 3
) -> RetrievalResponseDTO:
    """
    HYBRID SEMANTIC RETRIEVAL PIPELINE

    This function performs advanced semantic retrieval using:

    1. Multi-query expansion
    2. Dense vector similarity
    3. Metadata-aware scoring
    4. Cross-encoder reranking
    5. Hybrid score ranking
    6. Confidence filtering

    ============================================================
    PIPELINE OVERVIEW
    ============================================================

    USER QUERY
        ↓

    QUERY EXPANSION
        ↓

    EMBEDDING GENERATION
        ↓

    COSINE SIMILARITY SEARCH
        ↓

    METADATA BOOSTING
        ↓

    TOP-CANDIDATE SELECTION
        ↓

    CROSS-ENCODER RERANKING
        ↓

    HYBRID SCORING
        ↓

    CONFIDENCE FILTERING
        ↓

    FINAL TOP-K RESULTS

    ============================================================
    WHY THIS ARCHITECTURE IS STRONG
    ============================================================

    Cosine similarity:
        excellent recall

    Reranker:
        excellent precision

    Hybrid score:
        balances both

    Confidence filtering:
        reduces hallucinations

    Multi-query retrieval:
        improves semantic coverage
    """

    # ============================================================
    # 1. QUERY EXPANSION
    # ============================================================
    #
    # WHY IMPORTANT?
    # --------------
    # Users may ask the same concept differently.
    #
    # Example:
    #
    # Query:
    # "What is entanglement?"
    #
    # Expanded queries:
    # - "Explain quantum entanglement"
    # - "What does entangled state mean?"
    # - "Quantum particles correlation"
    #
    # This dramatically improves retrieval recall.
    # ============================================================

    expanded_queries: List[str] = expand_query(query)

    print(f"[RAG] expanded queries: {expanded_queries}")

    # ============================================================
    # 2. EMBED ALL QUERY VARIANTS
    # ============================================================
    #
    # Every expanded query becomes a vector.
    #
    # Later:
    # each chunk competes against ALL query vectors.
    #
    # We keep the BEST similarity score.
    # ============================================================

    query_embeddings: List[np.ndarray] = [
        np.array(
            embed_text(text=q, source="user_query")["embedding"]
        ) 
        for q in expanded_queries
        ]

    # ============================================================
    # RETRIEVAL ACCUMULATOR
    # ============================================================

    scored_chunks: List[RetrievalChunkDTO] = []

    print(f"[RAG] VECTOR_DB size: {len(VECTOR_DB)}")

    # ============================================================
    # 3. VECTOR SIMILARITY SEARCH
    # ============================================================
    #
    # Each stored chunk is compared against ALL expanded queries.
    #
    # We keep:
    # BEST(query ↔ chunk similarity)
    #
    # WHY?
    # ----
    # A chunk may align strongly with one wording
    # but weakly with another.
    #
    # Multi-query retrieval solves this.
    # ============================================================

    # ------------------------------------------------------------
    # BUILD QUERY EMBEDDING MATRIX
    # ------------------------------------------------------------
    # We embed multiple query variations (query expansion step)
    # into a single matrix so we can compare them in one operation.
    #
    # Shape:
    #   query_matrix → (Q, D)
    #   Q = number of expanded queries
    #   D = embedding dimension
    # ------------------------------------------------------------
    query_matrix = np.stack(query_embeddings)

    for chunk in VECTOR_DB:

        # ------------------------------------------------------------
        # LOAD DOCUMENT EMBEDDING
        # ------------------------------------------------------------
        # Each chunk already has a precomputed embedding stored in DB.
        # We convert it to numpy array for vector operations.
        #
        # Shape:
        #   doc_vec → (D,)
        # ------------------------------------------------------------
        doc_vec = np.array(chunk["embedding"])


        # ------------------------------------------------------------
        # VECTORISED COSINE SIMILARITY (FAST PATH)
        # ------------------------------------------------------------
        # Instead of looping over each query embedding (O(Q)),
        # we compute all similarities in a single matrix operation.
        #
        # Operation:
        #   query_matrix @ doc_vec → dot product for all queries
        #
        # Result:
        #   similarities → (Q,)
        #
        # Then we normalize using L2 norms to compute cosine similarity.
        # ------------------------------------------------------------
        query_norms = np.linalg.norm(query_matrix, axis=1)
        doc_norm = np.linalg.norm(doc_vec)

        similarities = (query_matrix @ doc_vec) / (query_norms * doc_norm + 1e-8)


        # ------------------------------------------------------------
        # SELECT BEST MATCH ACROSS ALL EXPANDED QUERIES
        # ------------------------------------------------------------
        # We assume:
        # - query expansion may produce paraphrases
        # - we want the strongest semantic match only
        #
        # So we take the maximum similarity score.
        # ------------------------------------------------------------
        cosine_score = float(np.max(similarities))

        # ========================================================
        # 4. FILTER LOW-QUALITY MATCHES
        # ========================================================
        #
        # WHY IMPORTANT?
        # --------------
        # Prevent garbage chunks from:
        # - entering reranker
        # - increasing noise
        # - polluting context
        #
        # This improves:
        # - precision
        # - speed
        # - hallucination resistance
        # ========================================================

        if cosine_score < MIN_SIMILARITY_SCORE:
            continue

        # ========================================================
        # 5. METADATA BOOSTING
        # ========================================================
        #
        # Metadata improves ranking quality.
        #
        # Example:
        # Query:
        # "Explain entanglement"
        #
        # Chunk concept:
        # "entanglement"
        #
        # → boost score
        #
        # WHY IMPORTANT?
        # --------------
        # Semantic similarity alone is not always enough.
        #
        # Metadata adds structured intelligence.
        # ========================================================

        metadata = chunk.get("metadata", {})

        metadata_bonus = 0.0

        concept = metadata.get("concept", "").lower()

        query_lower = query.lower()

        # --------------------------------------------------------
        # BOOST MATCHING CONCEPTS
        # --------------------------------------------------------

        if concept and concept in query_lower:
            metadata_bonus += 0.15

        # ========================================================
        # BUILD RETRIEVAL DTO
        # ========================================================

        scored_chunks.append(

            RetrievalChunkDTO(
                text=chunk["text"],

                source=metadata["source"]
                if metadata else "unknown",

                concept=metadata["concept"]
                if metadata else "unknown",

                length=metadata["length"]
                if metadata else 0,

                cosine_score=float(
                    cosine_score + metadata_bonus
                ),
            )
        )

    # ============================================================
    # 6. SORT BY COSINE SCORE
    # ============================================================
    #
    # This is the RECALL stage.
    #
    # Goal:
    # keep the most semantically relevant candidates.
    # ============================================================

    scored_chunks.sort(
        key=lambda x: x.cosine_score,
        reverse=True
    )

    # ============================================================
    # 7. EXPAND CANDIDATE POOL
    # ============================================================
    #
    # WHY IMPORTANT?
    # --------------
    # We intentionally keep MORE candidates
    # before reranking.
    #
    # If we only kept top_k immediately,
    # we could accidentally lose:
    # - semantically valuable chunks
    # - alternative explanations
    #
    # Cross-encoder reranking will later refine this.
    # ============================================================

    top_candidates = scored_chunks[:30]

    print(
        f"[RAG] candidates sent to reranker:"
        f" {len(top_candidates)}"
    )

    # ============================================================
    # 8. SAFE EMPTY RETRIEVAL HANDLING
    # ============================================================
    #
    # WHY IMPORTANT?
    # --------------
    # Prevent:
    # - reranker crashes
    # - empty inference calls
    # - downstream failures
    # ============================================================

    if not top_candidates:

        print("[RAG] no relevant candidates found")

        return RetrievalResponseDTO(results=[])

    # ============================================================
    # 9. CROSS-ENCODER RERANKING
    # ============================================================
    #
    # Dense retrieval:
    # good recall
    #
    # Cross-encoder:
    # high precision
    #
    # The reranker directly compares:
    #
    # (query, chunk)
    #
    # together in the SAME transformer.
    #
    # This is far more accurate.
    # ============================================================

    reranked: List[RetrievalChunkDTO] = rerank(
        query,
        top_candidates
    )

    # ============================================================
    # 10. SORT BY HYBRID SCORE
    # ============================================================
    #
    # Hybrid score combines:
    #
    # - rerank_score
    # - cosine_score
    #
    # WHY IMPORTANT?
    # --------------
    # Prevents reranker instability from
    # destroying strong semantic matches.
    # ============================================================

    reranked.sort(
        key=lambda x: x.hybrid_score,
        reverse=True
    )

    # ============================================================
    # DEBUG LOGGING
    # ============================================================

    for doc in reranked[:top_k]:

        print(
            f"[RAG]"
            f" source={doc.source}"
            f" cosine={doc.cosine_score:.4f}"
            f" rerank={doc.rerank_score:.4f}"
            f" hybrid={doc.hybrid_score:.4f}"
        )

    # ============================================================
    # 11. CONFIDENCE FILTERING
    # ============================================================
    #
    # WHY IMPORTANT?
    # --------------
    # Even top-ranked chunks may still be weak.
    #
    # If confidence is low:
    # → better to answer:
    #   "I don't know"
    #
    # than hallucinate.
    # ============================================================

    best_score = reranked[0].hybrid_score if reranked else 0.0

    action = decide_retrieval_action(best_score)

    print(f"[RAG] decision = {action}, score = {best_score:.4f}")

    if action == RetrievalAction.NO_RESULT:
        return RetrievalResponseDTO(results=[])

    if action == RetrievalAction.CLARIFY:
        return RetrievalResponseDTO(results=[])
    
    if action == RetrievalAction.RETRY:
        expanded = expand_query(query + " more context")
        return search_similar_documents(expanded[0], top_k)

    # ============================================================
    # 12. FINAL TOP-K RESULTS
    # ============================================================

    final_chunks = diversify_results(reranked, top_k=top_k)

    return RetrievalResponseDTO(
        results=final_chunks
    )