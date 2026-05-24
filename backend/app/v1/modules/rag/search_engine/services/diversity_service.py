from typing import List
from app.v1.modules.rag.retriever.diversity_filter import diversify_results
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

class DiversityService:
    @staticmethod
    def diversify(chunks: List[RetrievalChunkDTO], top_k: int)-> List[RetrievalChunkDTO]:
        return diversify_results(chunks, top_k)