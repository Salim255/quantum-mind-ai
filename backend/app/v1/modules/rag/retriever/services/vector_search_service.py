import numpy as np
from typing import List
import asyncio
import time
from qdrant_client import AsyncQdrantClient
from app.v1.modules.rag.retriever.services.scoring_service import ScoringService
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
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
    async def multi_query_qdrant_vector_search(
        cls,
        query: str,
        query_embeddings: List[np.ndarray],
        qdrant_client
    ) -> List[RetrievalChunkDTO]:
        
        # --------------------------------------------------------
        # STEP 1: PREPARE QUERY MATRIX
        # --------------------------------------------------------
        # Get candidate_chunks
        start =  time.perf_counter()

        candidates:List[DocumentDTO] = await cls.fetch_candidate_chunks_from_qdrant(
            query_embeddings,
            qdrant_client,
            limit=100
            )
        
        print("Perfoamnce check=====\n",  time.perf_counter() - start)
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
    async def fetch_candidate_chunks_from_qdrant(
        cls,
        query_embeddings: List[np.ndarray],  # List of query vectors (each query embedding from your model)
        qdrant_client: AsyncQdrantClient,          # Your Qdrant client instance (used to query vector DB)
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
       
  

        # --------------------------------------------------------
        # STEP 3: Execute ALL queries in parallel
        list_of_lists = await asyncio.gather(
            *[
                cls.qdrant_search(
                    query_embedding=emb,
                    qdrant_client=qdrant_client,
                    limit=limit
                )
                for emb in query_embeddings
            ]
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
    
    @classmethod
    def rank_qdrant_candidates(
        cls,
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

            doc_vec = np.array(chunk.embedding)

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

            results.append(cls.build_retrival_dto(chunk=chunk))

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
            id=point.id,
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
    def build_retrival_dto(chunk: DocumentDTO )->RetrievalChunkDTO:
        return RetrievalChunkDTO(
            text=chunk.text,
            source=chunk.metadata.source,
            concept=chunk.metadata.concept,
            length=chunk.metadata.length,
            cosine_score=chunk.cosine_score
        )

    @staticmethod
    async def qdrant_search(
            qdrant_client:AsyncQdrantClient,
            query_embedding: np.ndarray,
            limit: int
        ):
            """
            This function sends ONE query embedding to Qdrant
            and returns the matching points.
            """
            response = await qdrant_client.query_points(
                    collection_name="documents",   # Which collection to search in Qdrant
                    query=query_embedding.tolist(), # Convert numpy vector -> Python list (Qdrant format)
                    limit=limit,                    # Max number of results to return
                    with_vectors=True               # Include stored vectors in the response (needed for reranking later)
                )  
              
            return response.points 
                                     # Extract only the list of matching points
            