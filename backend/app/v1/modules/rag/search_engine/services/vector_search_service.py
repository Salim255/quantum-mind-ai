import numpy as np
from typing import List
from qdrant_client import QdrantClient
from app.v1.modules.rag.search_engine.services.scoring_service import ScoringService
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.vector_store.store import VECTOR_DB
from concurrent.futures import ThreadPoolExecutor  # Provides a pool of worker threads to run tasks in parallel
from app.db.qdrant import qdrant_to_dto
from qdrant_client.models import ScoredPoint
from app.v1.modules.rag.dto.document_dto import DocumentDTO, MetadataDTO

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
        # Get candidate_chunks
        candidates:List[DocumentDTO] = cls.fetch_candidate_chunks_from_qdrant(
            query_embeddings,
            qdrant_client,
            limit=100
            )
        
        print("Retrieved candidates:======\n", candidates)
        # --------------------------------------------------------
        # STEP 2: PREPARE QUERY MATRIX
        # --------------------------------------------------------
        # WHY:
        # Enables vectorized similarity computation
        query_matrix = cls.build_query_matrix(query_embeddings)
        ranked_candidates: List[RetrievalChunkDTO] = []

        ranked_candidates = cls.rank_qdrant_candidates(
            query,
            query_matrix,
            candidates
        )
        # =====================================================
        # FINAL RANKING
        # =====================================================
        return sorted(
            ranked_candidates,
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
            if cosine_score < MIN_SIMILARITY_SCORE:
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

    @classmethod
    def fetch_candidate_chunks_from_qdrant(
        cls,
        query_embeddings: List[np.ndarray],  # List of query vectors (each query embedding from your model)
        qdrant_client: QdrantClient,          # Your Qdrant client instance (used to query vector DB)
        limit: int = 100                      # Number of top results to retrieve per query
    )-> List[DocumentDTO]:
        """
        This function runs MULTIPLE Qdrant searches in PARALLEL
        instead of doing them one by one (sequentially).

        WHY THIS IS IMPORTANT:
        ----------------------
        - Each Qdrant request takes time (network + search latency)
        - Running them sequentially = slow
        - Running them in parallel = faster response time
        """
        merged_points: List[DocumentDTO] = []
        # ------------------------------------------------------------
        # STEP 1: Define a helper function (runs ONE Qdrant query)
        # ------------------------------------------------------------
        def search(query_embedding):
            """
            This function sends ONE query embedding to Qdrant
            and returns the matching points.
            """

            return (
                qdrant_client.query_points(
                    collection_name="documents",   # Which collection to search in Qdrant
                    query=query_embedding.tolist(), # Convert numpy vector -> Python list (Qdrant format)
                    limit=limit,                    # Max number of results to return
                    with_vectors=True               # Include stored vectors in the response (needed for reranking later)
                ).points                           # Extract only the list of matching points
            )

        # ------------------------------------------------------------
        # STEP 2: Create a thread pool (worker system)
        # ------------------------------------------------------------
        # max_workers=5 means:
        # → up to 5 Qdrant queries can run at the same time
        # → if you have more queries, they wait in queue
        # ------------------------------------------------------------
        with ThreadPoolExecutor(max_workers=5) as executor:

            # --------------------------------------------------------
            # STEP 3: Execute ALL queries in parallel
            # --------------------------------------------------------
            # executor.map does this:
            #
            # query_embeddings = [q1, q2, q3]
            #
            # runs:
            #   thread1 -> search(q1)
            #   thread2 -> search(q2)
            #   thread3 -> search(q3)
            #
            # ALL at the same time (not sequentially)
            # --------------------------------------------------------
            list_of_lists = list(
                executor.map(search, query_embeddings)
            )

        # ------------------------------------------------------------
        # STEP 3: FLATTEN results
        # from: [[points], [points], [points]]
        # to:   [point, point, point, ...]
        # ------------------------------------------------------------
        all_points = [
            cls.scored_point_to_document(point)
            for sublist in list_of_lists
            for point in sublist
        ]

        # ------------------------------------------------------------
        # STEP 4: DEDUPLICATE by point ID
        # (same document can appear in multiple queries)
        # ------------------------------------------------------------
        unique_points = {
            point.id: point
            for point in all_points
        }  # overwrites duplicates automatically

        # ------------------------------------------------------------
        # STEP 5: FINAL CLEAN LIST
        # ------------------------------------------------------------
        merged_points = list(unique_points.values())

        return merged_points
    
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
    
    @staticmethod
    def rank_qdrant_candidates(
        query: str,
        query_matrix,
        candidates: List[DocumentDTO]
    ) -> List[RetrievalChunkDTO]:

        results: List[RetrievalChunkDTO] = []

        # ------------------------------------------------------------
        # STEP 1: iterate over Qdrant candidates
        # ------------------------------------------------------------
        for chunk in candidates:

            # --------------------------------------------------------
            # STEP 2: cosine similarity against query embeddings
            # --------------------------------------------------------

            doc_vec = np.array(chunk["embedding"])

            similarities = ScoringService.compute_cosine_similarity(
                query_matrix,
                doc_vec
            )

            cosine_score = ScoringService.best_score(similarities)

            # --------------------------------------------------------
            # STEP 3: early filtering
            # --------------------------------------------------------
            if cosine_score < MIN_SIMILARITY_SCORE:
                continue

            # --------------------------------------------------------
            # STEP 4: metadata boosting
            # --------------------------------------------------------
            boosted_score: float = ScoringService.apply_metadata_boost(
                query=query,
                chunk=chunk,
                cosine_score=cosine_score
            )

            # --------------------------------------------------------
            # STEP 5: attach score to DTO
            # --------------------------------------------------------
            chunk.cosine_score = boosted_score

            results.append(chunk)

        # ------------------------------------------------------------
        # STEP 6: final ranking
        # ------------------------------------------------------------
        results.sort(
            key=lambda x: x.cosine_score,
            reverse=True
        )

        # ------------------------------------------------------------
        # STEP 7: top-K cut
        # ------------------------------------------------------------
        return results
    
    @staticmethod
    def scored_point_to_document(point: ScoredPoint) -> DocumentDTO:

        payload = point.payload or {}

        return DocumentDTO(
            text=payload["text"],
            embedding=point.vector,
            metadata=MetadataDTO(
                difficulty=payload.get("difficulty", "unknown"),
                source=payload.get("source", "unknown"),
                concept=payload.get("concept", "unknown"),
                length=payload.get("length", 0)
            )
        )

    @staticmethod
    def built_retrival_dto(chunk: DocumentDTO, cosine_score: float )->RetrievalChunkDTO:
        return RetrievalChunkDTO(
                    text=chunk["text"],
                    source=chunk["source"],
                    concept=chunk["concept"],
                    length=chunk["length"],
                    cosine_score=cosine_score
                )