from typing import List
import numpy as np
import time
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
from app.v1.modules.rag.retriever.decision_engine import RetrievalAction

class SearchEngineImpl(SearchEngineInterface):
    def search_similar_documents(
            self, 
            query: str, 
            top_k: int = 3
        )-> RetrievalResponseDTO:
        diversified = self.execute_pipeline(
            query=query,
            top_k=top_k
        )
      
        if not diversified:
            return RetrievalResponseDTO(results=[])
        
        # --------------------------------------------------------
        # STEP 7:
        # HANDLE RETRIEVAL DECISION
        # --------------------------------------------------------
        start = time.perf_counter()
        action: RetrievalAction = DecisionService.evaluate_retrieval_confidence(diversified)
        print("evaluate_retrieval_confidence___TIME:\n", time.perf_counter() - start)
        match action:
            case RetrievalAction.OK: 
                # --------------------------------------------------------
                # STEP 8:
                # RETURN FINAL RESULTS
                # --------------------------------------------------------
                return RetrievalResponseDTO(
                    results=diversified
                )
            case RetrievalAction.RETRY:
                # --------------------------------------------------------
                # Retry strategy:
                # - generate alternative queries
                # - broaden retrieval
                # - rerank again
                # --------------------------------------------------------
                #return self.handle_retry(
                #    query=query,
                #    top_k=top_k
                #) 
                return RetrievalResponseDTO(
                    results=diversified
                )
            
            case RetrievalAction.CLARIFY:
                # TODO
                return RetrievalResponseDTO(results=[])
            
            case _:
                 return RetrievalResponseDTO(results=[])
            
    # ---------------------------------------------------------
    # MAIN RETRIEVAL PIPELINE
    # ---------------------------------------------------------
    def execute_pipeline(
        self,
        query: str,
        top_k: int
    ) -> List[RetrievalChunkDTO]:

        candidates = self.retrieve_candidates(query)

        if not candidates:
            return []
    
        return self.post_process_candidates(
            query=query,
            candidates=candidates,
            top_k=top_k
        )
        
    # ---------------------------------------------------------
    # RETRIEVAL
    # ---------------------------------------------------------
    def retrieve_candidates(
        self,
        query: str
    ) -> List[RetrievalChunkDTO]:
        start = time.perf_counter()
        # 1. expand
        expanded_queries: List[str] = (
            QueryExpansionService.expand(query)
        )

        # 2. embed
        query_embeddings: List[np.ndarray] = (
            EmbeddingService.embed_expanded_queries(
                expanded_queries
            )
        )

        # 3. vector search
        print("retrieve_candidates TIME:____\n", time.perf_counter() - start)
        return VectorSearchService.multi_query_vector_search(
            query,
            query_embeddings
        )


    # ---------------------------------------------------------
    # POST PROCESSING
    # ---------------------------------------------------------
    def post_process_candidates(
        self,
        query: str,
        candidates: List[RetrievalChunkDTO],
        top_k: int
    ) -> List[RetrievalChunkDTO]:
        # 4. rerank
        reranked: List[RetrievalChunkDTO] = (
            RerankingService.rerank_candidates(
                query,
                candidates=candidates[:10]
            )
        )
        start = time.perf_counter()
        # 5. diversity
        diversified: List[RetrievalChunkDTO] = (
            DiversityService.diversify(
                reranked,
                top_k
            )
        )
        print("diversified TIME:____\n", time.perf_counter() - start)
        # 6. context roles
        ContextRoleService.assign_reasoning_roles(
            diversified
        )

        return diversified
    # ---------------------------------------------------------
    # RETRY HANDLER
    # ---------------------------------------------------------
    def handle_retry(
        self,
        query: str,
        top_k: int
    ) -> RetrievalResponseDTO:

        retry_results = self.execute_pipeline(
            query=query,
            top_k=top_k * 2
        )

        return RetrievalResponseDTO(
            results=retry_results
        )