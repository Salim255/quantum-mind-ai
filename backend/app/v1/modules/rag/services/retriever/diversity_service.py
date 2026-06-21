from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

class DiversityService: 
    # ============================================================
    # DIVERSITY FILTER
    # ============================================================
    # This module ensures that the final retrieved results:
    #
    # 1. Do NOT contain duplicate or near-duplicate chunks
    # 2. Cover multiple concepts instead of repeating one idea
    # 3. Preserve ranking quality from reranker
    #
    # WHY THIS MATTERS
    # -----------------
    # Without diversity filtering:
    # - LLM receives redundant context
    # - token space is wasted
    # - answer quality decreases (repetition bias)
    # ============================================================

    @staticmethod
    def diversify(
        chunks: List[RetrievalChunkDTO],
        max_per_concept: int = 1,
        top_k: int = 3
    ) -> List[RetrievalChunkDTO]:
        """
        Selects a diverse subset of top-ranked chunks.

        Strategy:
        ---------
        - Keep highest scoring chunks first
        - Remove duplicates
        - Limit repetition per concept
        - Preserve ranking order
        """

        selected: List[RetrievalChunkDTO] = []

        # ------------------------------------------------------------
        # Track already selected texts (hard deduplication)
        # ------------------------------------------------------------
        # WHY:
        # Prevent identical or near-identical chunk text from appearing
        # multiple times in final context.
        # ------------------------------------------------------------
        seen_texts = set()

        # ------------------------------------------------------------
        # Track concept frequency (diversity control)
        # ------------------------------------------------------------
        # WHY:
        # Prevent system from returning multiple chunks
        # from the same concept/topic.
        # ------------------------------------------------------------
        concept_count = {}

        for chunk in chunks:

            # Normalize text for deduplication
            text_key = chunk.text.strip().lower()

            # Extract concept safely
            concept = (chunk.concept or "unknown").lower()

            # --------------------------------------------------------
            # 1. HARD DEDUPLICATION CHECK
            # --------------------------------------------------------
            if text_key in seen_texts:
                continue

            # --------------------------------------------------------
            # 2. CONCEPT DIVERSITY LIMIT
            # --------------------------------------------------------
            if concept_count.get(concept, 0) >= max_per_concept:
                continue

            # --------------------------------------------------------
            # 3. ACCEPT CHUNK
            # --------------------------------------------------------
            selected.append(chunk)

            seen_texts.add(text_key)
            
            concept_count[concept] = concept_count.get(concept, 0) + 1

            # --------------------------------------------------------
            # 4. STOP EARLY IF WE REACHED TOP-K
            # --------------------------------------------------------
            if len(selected) >= top_k:
                break

        return selected
