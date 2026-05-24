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
from app.v1.modules.rag.context.context_builder import assign_context_role


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

class RAGSearchSimilar:
    @classmethod
    def search_similar_documents(
        cls,
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

        # print(f"[RAG] expanded queries: {expanded_queries}")

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
        # 7. EXPAND CANDIDATE POOL
        # ============================================================
        scored_chunks: List[RetrievalChunkDTO] = cls.perform_multi_query_vector_search(
            query=query, 
            query_embeddings=query_embeddings
            )
        
        top_candidates: List[RetrievalChunkDTO] = scored_chunks[:30]

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
        
        for i, chunk in enumerate(reranked):
            chunk.context_role = assign_context_role(chunk, i)

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
            return cls.search_similar_documents(expanded[0], top_k)

        # ============================================================
        # 12. FINAL TOP-K RESULTS
        # ============================================================

        final_chunks = diversify_results(reranked, top_k=top_k)

        return RetrievalResponseDTO(
            results=final_chunks
        )
    
    @staticmethod
    def build_query_matrix(
        query_embeddings: List[np.ndarray]
    )-> np.ndarray:
        """
        Convert multiple query embeddings into a single matrix.

        WHY IMPORTANT?
        --------------
        Vectorized matrix operations are significantly faster
        than nested Python loops.

        Shape
        -----
        (Q, D)

        Q:
            Number of expanded queries

        D:
            Embedding dimension
        """
        return np.stack(query_embeddings)
    
    
    @classmethod
    def score_document_against_queries(
        cls,
        query: str,
        chunk: dict,
        query_matrix: np.ndarray
    )-> RetrievalChunkDTO | None:
        """
        Compare one document against all expanded queries.

        RETURNS
        -------
        RetrievalChunkDTO
            Structured retrieval result

        None
            If similarity is below threshold
        """

        # ------------------------------------------------------------
        # LOAD DOCUMENT VECTOR
        # ------------------------------------------------------------
        document_vector = np.array(chunk["embedding"])

        # ------------------------------------------------------------
        # COMPUTE COSINE SIMILARITIES
        # ------------------------------------------------------------
        cosine_score = (
            cls.compute_best_cosine_similarity(
                query_matrix,
                document_vector
            )
        )

        # ------------------------------------------------------------
        # FILTER LOW-QUALITY MATCHES
        # ------------------------------------------------------------
        if cosine_score < MIN_SIMILARITY_SCORE:
            return None
        
        # ------------------------------------------------------------
        # APPLY METADATA BOOSTING
        # ------------------------------------------------------------
        boosted_score = (
            cls.apply_metadata_boost(
                query=query,
                chunk=chunk,
                cosine_score=cosine_score
            )
        )

        # ------------------------------------------------------------
        # BUILD DTO
        # ------------------------------------------------------------

        metadata = chunk.get("metadata", {})

        return RetrievalChunkDTO(
            text=chunk["text"],

            source=metadata.get("source", "unknown"),

            concept=metadata.get("concept", "unknown"),

            length=metadata.get("length", 0),

            cosine_score=boosted_score
        )
    
    @staticmethod
    def compute_best_cosine_similarity(
        query_matrix: np.ndarray,
        document_vector: np.ndarray
    )-> float:
        """
        Compute the best cosine similarity between
        a document and all expanded queries.

        WHY IMPORTANT?
        --------------
        Different query reformulations may match
        different semantic expressions inside documents.

        We keep ONLY the strongest semantic alignment.
        """

        query_norms = np.linalg.norm(
            query_matrix,
            axis=1
        )

        document_norm = np.linalg.norm(
            document_vector
        )

        similarities = (
            query_matrix @ document_vector
        ) / (
            query_norms * document_norm + 1e-8
        )

        return float(np.max(similarities))
        
    @staticmethod
    def apply_metadata_boost(
        query: str,
        chunk: dict,
        cosine_score: float
    )-> float:
        """
        Apply metadata-aware ranking bonuses.

        WHY IMPORTANT?
        --------------
        Pure semantic similarity is sometimes insufficient.

        Metadata provides structured retrieval signals:
        - concepts
        - trusted sources
        - tags
        - educational categories
        """

        metadata = chunk.get("metadata", {})


        concept = metadata.get(
            "concept",
            ""
        ).lower()

        query_lower = query.lower()

        metadata_bonus = 0.0

        # ------------------------------------------------------------
        # CONCEPT MATCH BOOST
        # ------------------------------------------------------------
        if concept and concept in query_lower:
            metadata_bonus += 0.15

        return cosine_score + metadata_bonus
    
    @staticmethod
    def rank_by_cosine_similarity(chunks: List[RetrievalChunkDTO])-> List[RetrievalChunkDTO]:
        """
        Sort retrieval candidates by cosine similarity.

        This represents the RECALL stage of retrieval.

        Higher similarity means:
        stronger semantic relevance.
        """

        chunks.sort(
            key=lambda x: x.cosine_score,
            reverse=True
        )
        
        return chunks
    
    @classmethod
    def perform_multi_query_vector_search(
        cls,
        query: str,
        query_embeddings: List[np.ndarray]
    )-> List[RetrievalChunkDTO]:
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

            scored_chunks = cls.score_document_against_queries(
                query=query,
                chunk=chunk, 
                query_matrix=query_matrix
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
        scored_chunks = cls.rank_by_cosine_similarity(scored_chunks)

        return scored_chunks