from typing import List
import numpy as np
from app.v1.modules.rag.dto.retrieval_dto import RetrievalResponseDTO
from app.v1.modules.rag.search_engine.services.query_expansion_service import QueryExpansionService
from app.v1.modules.rag.search_engine.services.vector_search_service import VectorSearchService
from app.v1.modules.rag.search_engine.services.reranking_service import RerankingService
from app.v1.modules.rag.search_engine.services.diversity_service import DiversityService
from app.v1.modules.rag.search_engine.services.context_role_service import ContextRoleService
from app.v1.modules.rag.search_engine.services.decision_service import DecisionService 
from app.v1.modules.rag.search_engine.services.embedding_service import EmbeddingService
from app.v1.modules.rag.search_engine.interfaces.search_engine_interface import SearchEngineInterface
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO

class SearchEngineImpl(SearchEngineInterface):
    def search_similar_documents(self, query: str,top_k: int = 3):
        # 1. expand
        expanded_queries: List[str] = QueryExpansionService.expand(query)

        # 2. embed
        query_embeddings: List[np.array] = EmbeddingService.embed_expanded_queries(expanded_queries)

        # 3. vector search
        candidates: List[RetrievalChunkDTO] = VectorSearchService.multi_query_vector_search(
            query,
            query_embeddings
        )

        if not candidates:
            return RetrievalResponseDTO(results=[])
        
        # 4. rerank
        reranked: List[RetrievalChunkDTO] = RerankingService.rerank_candidates(query, candidates)

        # 5. diversity
        diversified: List[RetrievalChunkDTO] = DiversityService.diversify(reranked, top_k)


        # 6. context roles
        ContextRoleService.assign_reasoning_roles(diversified)

        # --------------------------------------------------------
        # STEP 7:
        # HANDLE RETRIEVAL DECISION
        # --------------------------------------------------------
        action = DecisionService.evaluate_retrieval_confidence(diversified)

        if action == "NO_RESULT":
            return RetrievalResponseDTO(results=[])
        
         # --------------------------------------------------------
        # STEP 8:
        # RETURN FINAL RESULTS
        # --------------------------------------------------------
        return RetrievalResponseDTO(
            results=diversified
        )