from typing import List
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.retriever.reranker import rerank

class RerankingService:
    @staticmethod
    def rerank_candidates(
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

        reranked: List[RetrievalChunkDTO] = rerank(
            query,
            candidates
        )

        reranked.sort(
            key=lambda chunk: chunk.hybrid_score,
            reverse=True
        )

        return reranked