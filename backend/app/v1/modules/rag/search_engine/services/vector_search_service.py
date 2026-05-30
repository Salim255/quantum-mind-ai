import numpy as np
from typing import List
from qdrant_client import QdrantClient
from app.v1.modules.rag.search_engine.services.scoring_service import ScoringService
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.vector_store.store import VECTOR_DB

MIN_SIMILARITY_SCORE = 0.25

class VectorSearchService:
    """
    VECTOR SEARCH ENGINE (CORE RETRIEVAL LAYER)
    ===========================================

    RESPONSIBILITY:
    --------------
    - compare query embeddings vs document embeddings
    - compute similarity scores
    - apply ranking + metadata boosting
    - return top-k candidates

    WHAT IT MUST NOT DO:
    --------------------
    - query expansion
    - concept detection
    - NLP logic
    """

    MIN_SIMILARITY_SCORE = 0.25

    @classmethod
    def multi_query_qdrant_vector_search(
        cls,
        query: str,
        query_embeddings: List[np.ndarray],
        qdrant_client
    ) -> List[RetrievalChunkDTO]:

        # --------------------------------------------------------
        # STEP 1: PREPARE QUERY MATRIX
        # --------------------------------------------------------
        # WHY:
        # Enables vectorized similarity computation
        query_matrix = cls.build_query_matrix(query_embeddings)

        results: List[RetrievalChunkDTO] = []
        # =====================================================
        # SEARCH EACH QUERY VECTOR
        # =====================================================
        for query_embedding in query_embeddings:

            search_results = qdrant_client.query_points(
                collection_name="documents",
                query=query_embedding.tolist(),
                limit=20,
                with_vectors=False
            )

            print("Test data of search_results===== \n",search_results)
            for hit in search_results.points:
                cosine_score = hit.score
            
                # ---------------------------------------------
                # EARLY FILTERING
                # ---------------------------------------------
                if cosine_score < cls.MIN_SIMILARITY_SCORE:
                    continue

                payload = hit.payload

                # ---------------------------------------------
                # METADATA BOOSTING
                # ---------------------------------------------
                boosted_score = (
                    ScoringService.apply_metadata_boost(
                        query=query,
                        chunk=payload,
                        cosine_score=cosine_score
                    )
                )

                results.append(
                    RetrievalChunkDTO(
                        text=payload.get("text", ""),
                        source=payload.get("source", "unknown"),
                        concept=payload.get("concept", "unknown"),
                        length=payload.get("length", 0),
                        cosine_score=boosted_score
                    )
                )

        # =====================================================
        # FINAL RANKING
        # =====================================================
        return sorted(
            results,
            key=lambda x: x.cosine_score,
            reverse=True
        )
    
    @classmethod
    def multi_query_vector_search(
        cls,
        query: str,
        query_embeddings: List[np.ndarray]
    ) -> List[RetrievalChunkDTO]:

        # --------------------------------------------------------
        # STEP 1: PREPARE QUERY MATRIX
        # --------------------------------------------------------
        # WHY:
        # Enables vectorized similarity computation
        query_matrix = cls.build_query_matrix(query_embeddings)

        results: List[RetrievalChunkDTO] = []

        # --------------------------------------------------------
        # STEP 2: SCAN VECTOR DATABASE
        # --------------------------------------------------------
        # NOTE:
        # This is linear scan (OK for small scale, replace later
        # with FAISS / HNSW for production scale)
        # --------------------------------------------------------
        for chunk in VECTOR_DB:

            doc_vec = np.array(chunk["embedding"])

            # ----------------------------------------------------
            # STEP 2A: COSINE SIMILARITY
            # ----------------------------------------------------
            similarities = ScoringService.compute_cosine_similarity(
                query_matrix,
                doc_vec
            )

            cosine_score = ScoringService.best_score(similarities)

            # ----------------------------------------------------
            # STEP 2B: EARLY FILTERING
            # ----------------------------------------------------
            # WHY:
            # Remove obviously irrelevant chunks early
            if cosine_score < cls.MIN_SIMILARITY_SCORE:
                continue

            # ----------------------------------------------------
            # STEP 2C: METADATA BOOSTING
            # ----------------------------------------------------
            # WHY:
            # Injects weak semantic signals like:
            # - concept match
            # - source relevance
            boosted_score = ScoringService.apply_metadata_boost(
                query=query,
                chunk=chunk,
                cosine_score=cosine_score
            )

            metadata = chunk.get("metadata", {})

            # ----------------------------------------------------
            # STEP 2D: BUILD DTO
            # ----------------------------------------------------
            results.append(
                RetrievalChunkDTO(
                    text=chunk["text"],
                    source=metadata.get("source", "unknown"),
                    concept=metadata.get("concept", "unknown"),
                    length=metadata.get("length", 0),
                    cosine_score=boosted_score
                )
            )

        # --------------------------------------------------------
        # STEP 3: FINAL RANKING
        # --------------------------------------------------------
        # WHY:
        # Highest scoring chunks should be returned first
        return sorted(
            results,
            key=lambda x: x.cosine_score,
            reverse=True
        )

    @staticmethod
    def fetch_candidate_chunks_from_qdrant(
        cls,
        query_embeddings: List[np.ndarray],
        qdrant_client: QdrantClient,
        limit: int = 100
    ):
        all_search_results = []
        for query_embedding in query_embeddings:

            search_results = qdrant_client.query_points(
                collection_name="documents",
                query=query_embedding.tolist(),
                limit=limit,
                with_vectors=True
            )

            all_search_results.append(
                search_results.points
            )
    # ============================================================
    # QUERY MATRIX BUILDER
    # ============================================================
    @staticmethod
    def build_query_matrix(
        query_embeddings: List[np.ndarray]
    ) -> np.ndarray:
        """
        Convert list of query embeddings into matrix form.

        WHY THIS EXISTS:
        --------------
        Enables batch similarity computation instead of loops.
        """

        return np.stack(query_embeddings)