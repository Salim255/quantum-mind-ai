from time import time
from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------
# Controls batching size for inference safety.
# Large batches can cause:
# - memory spikes
# - GPU/CPU saturation
# ------------------------------------------------------------
BATCH_SIZE = 32

class RerankingService:
    def __init__(self, container):
        self.container = container

    def rerank_candidates(
            self,
            query: str,
            candidates: List[RetrievalChunkDTO]
        )-> List[RetrievalChunkDTO]:
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
        
        reranked: List[RetrievalChunkDTO] = self.rerank(
            query,
            candidates
        )

        reranked.sort(
            key=lambda chunk: chunk.hybrid_score,
            reverse=True
        )

        return reranked
    

    def rerank(
            self, 
            query: str, 
            docs: List[RetrievalChunkDTO]
        ) ->  List[RetrievalChunkDTO]:
        """
        Re-ranks retrieved documents using a cross-encoder model.

        This step improves precision by re-evaluating
        semantic relevance between query and documents.

        Parameters
        ----------
        query : str
            User question.

        docs : List[RetrievalChunkDTO]
            Candidate chunks from vector search.

        Returns
        -------
        List[RetrievalChunkDTO]
            Same objects enriched with rerank_score,
            sorted by final relevance.
        """

        # ------------------------------------------------------------
        # 1. BUILD QUERY-DOCUMENT PAIRS
        # ------------------------------------------------------------
        # We convert retrieval candidates into model input format.
        # Each pair is independently scored by the cross-encoder.
        # ------------------------------------------------------------
        pairs = [(query, doc.text) for doc in docs]
        

        # ------------------------------------------------------------
        # 2. BATCHED PREDICTION
        # ------------------------------------------------------------
        # We avoid sending all pairs at once to prevent:
        # - memory overload
        # - inference instability
        # ------------------------------------------------------------
        all_scores: List[float] = []

        for i in range(0, len(pairs), BATCH_SIZE):
            batch = pairs[i:i + BATCH_SIZE]

            batch_scores = self.container.reranker.predict(batch)

            # Ensure consistent Python list type
            all_scores.extend(list(batch_scores))


        # ------------------------------------------------------------
        # 3. ATTACH SCORES TO DTOs (NO STRUCTURE CHANGE)
        # ------------------------------------------------------------
        # We mutate only score fields, not structure.
        # This keeps pipeline compatible with later stages.
        # ------------------------------------------------------------
        for doc, score in zip(docs, all_scores):
            doc.rerank_score = float(score)

        # ------------------------------------------------------------
        # 4. COMPUTE HYBRID SCORE (FINAL SCORING LAYER)
        # ------------------------------------------------------------
        # Hybrid scoring balances:
        # - reranker precision (semantic understanding)
        # - cosine recall safety (embedding similarity)
        # ------------------------------------------------------------
        for doc in docs:
            doc.hybrid_score = (
                0.7 * (doc.rerank_score or 0.0) +
                0.3 * (doc.cosine_score or 0.0)
            )

        # ------------------------------------------------------------
        # 5. FINAL SORTING (PRIMARY SIGNAL = RERANK SCORE)
        # ------------------------------------------------------------
        docs.sort(key=lambda x: x.rerank_score or 0.0, reverse=True)
    
        return docs