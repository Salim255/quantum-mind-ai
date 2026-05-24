import numpy as np

from typing import List

from app.v1.modules.rag.embeddings.embedder import embed_text
from app.v1.modules.rag.vector_store.store import VECTOR_DB

from app.v1.modules.rag.retriever.query_expander import expand_query
from app.v1.modules.rag.retriever.reranker import rerank

from app.v1.modules.rag.retriever.decision_engine import (
    decide_retrieval_action,
    RetrievalAction
)

from app.v1.modules.rag.retriever.diversity_filter import (
    diversify_results
)

from app.v1.modules.rag.context.context_builder import (
    assign_context_role
)

from app.v1.modules.rag.dto.retrieval_dto import (
    RetrievalChunkDTO,
    RetrievalResponseDTO
)


# ============================================================
# RETRIEVAL CONFIGURATION
# ============================================================

# ------------------------------------------------------------
# MINIMUM COSINE SIMILARITY
# ------------------------------------------------------------
#
# Chunks below this score are ignored BEFORE reranking.
#
# WHY IMPORTANT?
# --------------
# Prevents:
# - noisy retrieval
# - useless reranker computation
# - irrelevant context pollution
# - hallucination amplification
#
# This is the FIRST retrieval quality gate.
# ------------------------------------------------------------
MIN_SIMILARITY_SCORE = 0.25


# ------------------------------------------------------------
# MAX CANDIDATES FOR RERANKING
# ------------------------------------------------------------
#
# We intentionally keep more chunks than final top_k.
#
# WHY IMPORTANT?
# --------------
# Dense retrieval is optimized for RECALL.
#
# The reranker later improves PRECISION.
#
# Keeping a larger candidate pool helps avoid:
# - missing hidden relevant chunks
# - losing alternative explanations
# - weak retrieval coverage
# ------------------------------------------------------------
MAX_RERANK_CANDIDATES = 30


# ============================================================
# SEMANTIC SEARCH ENGINE
# ============================================================
#
# RESPONSIBILITY
# --------------
# This class handles the COMPLETE retrieval pipeline:
#
# 1. Query expansion
# 2. Query embedding generation
# 3. Multi-query vector retrieval
# 4. Metadata-aware scoring
# 5. Reranking
# 6. Diversity filtering
# 7. Context role assignment
# 8. Retrieval confidence decisions
#
# ARCHITECTURE GOAL
# -----------------
# Build a retrieval system that is:
#
# - modular
# - scalable
# - explainable
# - hallucination resistant
# - easy to debug
# - production maintainable
# ============================================================
class RAGSearchSimilar:

    # ============================================================
    # MAIN ENTRY POINT
    # ============================================================
    @classmethod
    def search_similar_documents(
        cls,
        query: str,
        top_k: int = 3
    ) -> RetrievalResponseDTO:
        """
        Execute the complete semantic retrieval pipeline.

        PIPELINE OVERVIEW
        -----------------

        USER QUERY
            ↓

        QUERY EXPANSION
            ↓

        QUERY EMBEDDING
            ↓

        VECTOR SEARCH
            ↓

        CANDIDATE FILTERING
            ↓

        CROSS-ENCODER RERANKING
            ↓

        HYBRID RANKING
            ↓

        DIVERSITY FILTERING
            ↓

        CONTEXT ROLE ASSIGNMENT
            ↓

        FINAL TOP-K RESULTS
        """

        # --------------------------------------------------------
        # STEP 1:
        # EXPAND USER QUERY
        # --------------------------------------------------------
        expanded_queries = cls.expand_user_query(query)

        # --------------------------------------------------------
        # STEP 2:
        # GENERATE QUERY EMBEDDINGS
        # --------------------------------------------------------
        query_embeddings = cls.embed_expanded_queries(
            expanded_queries
        )

        # --------------------------------------------------------
        # STEP 3:
        # PERFORM MULTI-QUERY VECTOR SEARCH
        # --------------------------------------------------------
        retrieved_chunks = cls.perform_multi_query_vector_search(
            query=query,
            query_embeddings=query_embeddings
        )

        # --------------------------------------------------------
        # STEP 4:
        # KEEP BEST RETRIEVAL CANDIDATES
        # --------------------------------------------------------
        top_candidates = cls.select_top_candidates(
            retrieved_chunks
        )

        # --------------------------------------------------------
        # STEP 5:
        # HANDLE EMPTY RETRIEVAL
        # --------------------------------------------------------
        if not top_candidates:

            print("[RAG] no relevant candidates found")

            return RetrievalResponseDTO(results=[])

        # --------------------------------------------------------
        # STEP 6:
        # CROSS-ENCODER RERANKING
        # --------------------------------------------------------
        reranked_chunks = cls.rerank_candidates(
            query=query,
            candidates=top_candidates
        )

        # --------------------------------------------------------
        # STEP 7:
        # HANDLE RETRIEVAL DECISION
        # --------------------------------------------------------
        action = cls.evaluate_retrieval_confidence(
            reranked_chunks
        )

        if action == RetrievalAction.NO_RESULT:
            return RetrievalResponseDTO(results=[])

        if action == RetrievalAction.CLARIFY:
            return RetrievalResponseDTO(results=[])

        # --------------------------------------------------------
        # STEP 8:
        # REMOVE SEMANTIC DUPLICATES
        # --------------------------------------------------------
        diversified_chunks = diversify_results(
            reranked_chunks,
            top_k=top_k
        )

        # --------------------------------------------------------
        # STEP 9:
        # ASSIGN CONTEXT ROLES
        # --------------------------------------------------------
        cls.assign_reasoning_roles(
            diversified_chunks
        )

        # --------------------------------------------------------
        # STEP 10:
        # DEBUG LOGGING
        # --------------------------------------------------------
        cls.log_final_results(diversified_chunks)

        # --------------------------------------------------------
        # STEP 11:
        # RETURN FINAL RESULTS
        # --------------------------------------------------------
        return RetrievalResponseDTO(
            results=diversified_chunks
        )

    # ============================================================
    # QUERY EXPANSION
    # ============================================================
    @staticmethod
    def expand_user_query(query: str) -> List[str]:
        """
        Expand a user query into multiple semantic variations.

        WHY IMPORTANT?
        --------------
        Users can describe the same concept differently.

        Example:
        --------
        Original:
            "What is quantum entanglement?"

        Expanded:
            - "Explain quantum entanglement"
            - "What is an entangled quantum state?"
            - "Quantum particle correlation"

        BENEFITS
        --------
        Improves:
        - semantic recall
        - retrieval coverage
        - robustness to phrasing variation
        """

        expanded_queries = expand_query(query)

        print(f"[RAG] expanded queries: {expanded_queries}")

        return expanded_queries

    # ============================================================
    # QUERY EMBEDDING
    # ============================================================
    @staticmethod
    def embed_expanded_queries(
        expanded_queries: List[str]
    ) -> List[np.ndarray]:
        """
        Convert expanded queries into embedding vectors.

        RETURNS
        -------
        List[np.ndarray]

        Example:
        --------
        [
            [0.12, 0.44, 0.91],
            [0.66, 0.28, 0.77],
            [0.31, 0.85, 0.55]
        ]

        WHY IMPORTANT?
        --------------
        Embeddings convert semantic meaning into vector space,
        enabling mathematical similarity comparison.
        """

        return [
            np.array(
                embed_text(
                    text=query,
                    source="user_query"
                )["embedding"]
            )
            for query in expanded_queries
        ]

    # ============================================================
    # MULTI-QUERY VECTOR SEARCH
    # ============================================================
    @classmethod
    def perform_multi_query_vector_search(
        cls,
        query: str,
        query_embeddings: List[np.ndarray]
    ) -> List[RetrievalChunkDTO]:
        """
        Search the vector database using ALL expanded queries.

        WHY IMPORTANT?
        --------------
        Different query variations may match different chunks.

        We retrieve chunks using:
        BEST(query ↔ chunk similarity)
        """

        scored_chunks: List[RetrievalChunkDTO] = []

        print(f"[RAG] VECTOR_DB size: {len(VECTOR_DB)}")

        # --------------------------------------------------------
        # BUILD QUERY MATRIX
        # --------------------------------------------------------
        query_matrix = cls.build_query_matrix(
            query_embeddings
        )

        # --------------------------------------------------------
        # SCORE ALL DOCUMENTS
        # --------------------------------------------------------
        for chunk in VECTOR_DB:

            scored_chunk = cls.score_document_against_queries(
                query=query,
                chunk=chunk,
                query_matrix=query_matrix
            )

            if scored_chunk:
                scored_chunks.append(scored_chunk)

        # --------------------------------------------------------
        # SORT BY SEMANTIC SIMILARITY
        # --------------------------------------------------------
        return cls.rank_by_cosine_similarity(
            scored_chunks
        )

    # ============================================================
    # QUERY MATRIX CONSTRUCTION
    # ============================================================
    @staticmethod
    def build_query_matrix(
        query_embeddings: List[np.ndarray]
    ) -> np.ndarray:
        """
        Convert multiple embedding vectors into one matrix.

        WHY IMPORTANT?
        --------------
        Vectorized matrix operations are significantly faster
        than looping through embeddings individually.

        INPUT
        -----
        [
            [0.11, 0.55, 0.91],
            [0.22, 0.88, 0.33],
            [0.44, 0.66, 0.77]
        ]

        OUTPUT
        ------
        Matrix shape:
            (Q, D)

        Q = number of queries
        D = embedding dimensions
        """

        return np.stack(query_embeddings)

    # ============================================================
    # DOCUMENT SCORING
    # ============================================================
    @classmethod
    def score_document_against_queries(
        cls,
        query: str,
        chunk: dict,
        query_matrix: np.ndarray
    ) -> RetrievalChunkDTO:
        """
        Compare one document against all expanded queries.

        RETURNS
        -------
        RetrievalChunkDTO
            if relevant

        None
            if similarity is too low
        """

        # --------------------------------------------------------
        # LOAD DOCUMENT VECTOR
        # --------------------------------------------------------
        document_vector = np.array(
            chunk["embedding"]
        )

        # --------------------------------------------------------
        # COMPUTE BEST COSINE SIMILARITY
        # --------------------------------------------------------
        cosine_score = cls.compute_best_cosine_similarity(
            query_matrix=query_matrix,
            document_vector=document_vector
        )

        # --------------------------------------------------------
        # FILTER LOW QUALITY RESULTS
        # --------------------------------------------------------
        if cosine_score < MIN_SIMILARITY_SCORE:
            return None

        # --------------------------------------------------------
        # APPLY METADATA BOOSTING
        # --------------------------------------------------------
        boosted_score = cls.apply_metadata_boost(
            query=query,
            chunk=chunk,
            cosine_score=cosine_score
        )

        # --------------------------------------------------------
        # BUILD DTO
        # --------------------------------------------------------
        metadata = chunk.get("metadata", {})

        return RetrievalChunkDTO(
            text=chunk["text"],

            source=metadata.get(
                "source",
                "unknown"
            ),

            concept=metadata.get(
                "concept",
                "unknown"
            ),

            length=metadata.get(
                "length",
                0
            ),

            cosine_score=boosted_score
        )

    # ============================================================
    # COSINE SIMILARITY
    # ============================================================
    @staticmethod
    def compute_best_cosine_similarity(
        query_matrix: np.ndarray,
        document_vector: np.ndarray
    ) -> float:
        """
        Compute the BEST semantic similarity between:
        - one document
        - all expanded queries

        WHY IMPORTANT?
        --------------
        Some query reformulations may align better with
        specific document wording.

        We keep ONLY the strongest semantic match.
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

    # ============================================================
    # METADATA BOOSTING
    # ============================================================
    @staticmethod
    def apply_metadata_boost(
        query: str,
        chunk: dict,
        cosine_score: float
    ) -> float:
        """
        Improve ranking using structured metadata.

        WHY IMPORTANT?
        --------------
        Semantic similarity alone is not always enough.

        Metadata adds:
        - concept awareness
        - educational structure
        - domain intelligence
        """

        metadata = chunk.get("metadata", {})

        concept = metadata.get(
            "concept",
            ""
        ).lower()

        query_lower = query.lower()

        metadata_bonus = 0.0

        # --------------------------------------------------------
        # CONCEPT MATCH BOOST
        # --------------------------------------------------------
        if concept and concept in query_lower:
            metadata_bonus += 0.15

        return cosine_score + metadata_bonus

    # ============================================================
    # COSINE RANKING
    # ============================================================
    @staticmethod
    def rank_by_cosine_similarity(
        chunks: List[RetrievalChunkDTO]
    ) -> List[RetrievalChunkDTO]:
        """
        Sort retrieval results by semantic similarity.

        This is the RECALL stage.
        """

        chunks.sort(
            key=lambda chunk: chunk.cosine_score,
            reverse=True
        )

        return chunks

    # ============================================================
    # TOP CANDIDATE SELECTION
    # ============================================================
    @staticmethod
    def select_top_candidates(
        chunks: List[RetrievalChunkDTO]
    ) -> List[RetrievalChunkDTO]:
        """
        Select best retrieval candidates before reranking.

        WHY IMPORTANT?
        --------------
        Rerankers are expensive.

        We first reduce search space using:
        semantic similarity ranking.
        """

        candidates = chunks[:MAX_RERANK_CANDIDATES]

        print(
            "[RAG] candidates sent to reranker:"
            f" {len(candidates)}"
        )

        return candidates

    # ============================================================
    # CROSS-ENCODER RERANKING
    # ============================================================
    @staticmethod
    def rerank_candidates(
        query: str,
        candidates: List[RetrievalChunkDTO]
    ) -> List[RetrievalChunkDTO]:
        """
        Improve retrieval precision using cross-encoder reranking.

        WHY IMPORTANT?
        --------------
        Dense retrieval:
            excellent recall

        Cross-encoder:
            excellent precision

        The reranker evaluates:
            (query, chunk)

        together inside the SAME transformer model.
        """

        reranked = rerank(
            query,
            candidates
        )

        reranked.sort(
            key=lambda chunk: chunk.hybrid_score,
            reverse=True
        )

        return reranked

    # ============================================================
    # RETRIEVAL DECISION ENGINE
    # ============================================================
    @staticmethod
    def evaluate_retrieval_confidence(
        chunks: List[RetrievalChunkDTO]
    ) -> RetrievalAction:
        """
        Decide whether retrieval quality is sufficient.

        WHY IMPORTANT?
        --------------
        Weak retrieval causes hallucinations.

        Better to:
            say "I don't know"

        than generate misinformation.
        """

        best_score = (
            chunks[0].hybrid_score
            if chunks
            else 0.0
        )

        action = decide_retrieval_action(
            best_score
        )

        print(
            f"[RAG] decision={action}"
            f" score={best_score:.4f}"
        )

        return action

    # ============================================================
    # CONTEXT ROLE ASSIGNMENT
    # ============================================================
    @staticmethod
    def assign_reasoning_roles(
        chunks: List[RetrievalChunkDTO]
    ) -> None:
        """
        Assign reasoning roles to retrieved chunks.

        Example roles:
        --------------
        - core
        - supporting
        - example

        WHY IMPORTANT?
        --------------
        Ordered reasoning context improves:
        - answer coherence
        - explanation quality
        - logical grounding
        """

        for index, chunk in enumerate(chunks):

            chunk.context_role = assign_context_role(
                chunk,
                index
            )

    # ============================================================
    # DEBUG LOGGING
    # ============================================================
    @staticmethod
    def log_final_results(
        chunks: List[RetrievalChunkDTO]
    ) -> None:
        """
        Print final retrieval diagnostics.

        WHY IMPORTANT?
        --------------
        Retrieval debugging is critical in RAG systems.

        Logs help diagnose:
        - ranking issues
        - hallucinations
        - weak retrieval
        - reranker instability
        """

        for chunk in chunks:

            print(
                f"[RAG]"
                f" source={chunk.source}"
                f" cosine={chunk.cosine_score:.4f}"
                f" rerank={chunk.rerank_score:.4f}"
                f" hybrid={chunk.hybrid_score:.4f}"
            )