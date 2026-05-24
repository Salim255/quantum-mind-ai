import numpy as np
from typing import List
from app.v1.modules.rag.search_engine.services.scoring_service import ScoringService
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.vector_store.store import VECTOR_DB

MIN_SIMILARITY_SCORE = 0.25

class VectorSearchService:
    @classmethod
    def multi_query_vector_search(
        cls,
        query: str, 
        query_embeddings: List[np.ndarray]
        )-> RetrievalChunkDTO:
        query_matrix = cls.build_query_matrix(query_embeddings)

        results: List[RetrievalChunkDTO] = []

        for chunk in VECTOR_DB:

            doc_vec = np.array(chunk["embedding"])

            similarities = ScoringService.compute_cosine_similarity(
                query_matrix,
                doc_vec
            )

            cosine_score = ScoringService.best_score(similarities)

            if cosine_score < MIN_SIMILARITY_SCORE:
                continue

            # --------------------------------------------------------
            # APPLY METADATA BOOSTING
            # --------------------------------------------------------
            boosted_score = ScoringService.apply_metadata_boost(
                query=query,
                chunk=chunk,
                cosine_score=cosine_score
            )
            metadata = chunk.get("metadata", {})

            results.append(
                RetrievalChunkDTO(
                    text=chunk["text"],
                    source=metadata.get("source", "unknown"),
                    concept=metadata.get("concept", "unknown"),
                    length=metadata.get("length", 0),
                    cosine_score=boosted_score
                )
            )

        return sorted(results, key=lambda x: x.cosine_score, reverse=True)

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
    
    