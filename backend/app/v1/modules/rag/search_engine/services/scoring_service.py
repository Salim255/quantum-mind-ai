import numpy as np
class ScoringService:
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