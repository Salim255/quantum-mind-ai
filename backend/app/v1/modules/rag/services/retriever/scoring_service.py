import numpy as np
class ScoringService:
    @staticmethod
    def compute_cosine_similarity(
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

        similarities: float = (
            query_matrix @ document_vector
        ) / (
            query_norms * document_norm + 1e-8
        )

        return similarities
    
    
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
  
        # --------------------------------------------------------
        # NORMALIZE METADATA ACCESS (dict + Qdrant compatible)
        # --------------------------------------------------------

        # Case 1: dict (local VECTOR_DB)
        if isinstance(chunk, dict):
            metadata = chunk.get("metadata", {})

        # Case 2: Qdrant ScoredPoint
        else:
            metadata = getattr(chunk, "payload", {})

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
    
    @staticmethod
    def best_score(similarities):
        return float(np.max(similarities))