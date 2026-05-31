from typing import List
import numpy as np
from app.v1.modules.rag.dto.retrieval_dto import RetrievalResponseDTO
from app.v1.modules.rag.retriever.services.query_expansion_service import QueryExpansionService
from app.v1.modules.rag.retriever.services.vector_search_service import VectorSearchService
from app.v1.modules.rag.retriever.services.reranking_service import RerankingService
from app.v1.modules.rag.retriever.services.diversity_service import DiversityService
from app.v1.modules.rag.retriever.services.context_role_service import ContextRoleService
from app.v1.modules.rag.retriever.services.decision_service import DecisionService
from app.v1.modules.rag.retriever.services.embedding_service import EmbeddingService
from app.v1.modules.rag.retriever.interfaces.search_engine_interface import RetrieverInterface
from app.v1.modules.rag.dto.retrieval_dto import RetrievalChunkDTO
from app.v1.modules.rag.dto.query_analysis_result_dto import QueryAnalysisResultDto
from app.v1.modules.rag.retriever.services.decision_service import RetrievalAction
from app.core.container import Container
from app.v1.modules.rag.retriever.services.query_analysis_service import QueryAnalysisService

class RetrieverImpl(RetrieverInterface):
    def __init__(
            self, 
            container: Container,
            reranking_service: RerankingService,
            embedding_service: EmbeddingService
        
        ):
        self.reranking_service = reranking_service
        self.container = container
        self.embedding_service = embedding_service

    def search_similar_documents(
            self, 
            query: str, 
            top_k: int = 3
        )-> RetrievalResponseDTO:

        diversified:List[RetrievalChunkDTO] = self.execute_pipeline(
            query=query,
            top_k=top_k
        )
      
        if not diversified:
            return RetrievalResponseDTO(results=[])
        
        # --------------------------------------------------------
        # STEP 7:
        # HANDLE RETRIEVAL DECISION
        # --------------------------------------------------------
    
        action: RetrievalAction = DecisionService.evaluate_retrieval_confidence(diversified)
        
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
                return RetrievalResponseDTO(
                    results=diversified
                )
            
            
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

        # candidates = self.retrieve_candidates(query)

        candidates: List[RetrievalChunkDTO] = self.retrieve_qdrant_candidates(query=query)
        if not candidates:
            return []
    
        return self.post_process_candidates(
            query=query,
            candidates=candidates[:10],
            top_k=top_k
        )
        
    # ---------------------------------------------------------
    # RETRIEVAL
    # ---------------------------------------------------------
    def retrieve_candidates(
        self,
        query: str
    ) -> List[RetrievalChunkDTO]:
        
        analysis: QueryAnalysisResultDto = QueryAnalysisService.detect(query)

        expanded_queries: List[str]

        # 1. expand
        if analysis.requires_expansion:
            expanded_queries = (
                QueryExpansionService.expand(query)
            )
        else:
            expanded_queries = [query]
        
        # 2. embed
        query_embeddings: List[np.ndarray] = (
            self.embedding_service.embed_expanded_queries(
                expanded_queries
            )
        )

        # 3. vector search
        return VectorSearchService.multi_query_vector_search(
            query,
            query_embeddings
        )

    def retrieve_qdrant_candidates(
        self,
        query: str
    ) -> List[RetrievalChunkDTO]:
        
        analysis: QueryAnalysisResultDto = QueryAnalysisService.detect(query)

        expanded_queries: List[str]

        # 1. expand
        if analysis.requires_expansion:
            expanded_queries = (
                QueryExpansionService.expand(query)
            )
        else:
            expanded_queries = [query]
        
        # 2. embed
        query_embeddings: List[np.ndarray] = (
            self.embedding_service.embed_expanded_queries(
                expanded_queries
            )
        )

        # 3. vector search
        return VectorSearchService.multi_query_qdrant_vector_search(
            query=query,
            query_embeddings=query_embeddings,
            qdrant_client=self.container.qdrant.client
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
        reranked: List[RetrievalChunkDTO] = self.reranking_service.rerank_candidates(
                query,
                candidates=candidates
            )
      
        # 5. diversity
        diversified: List[RetrievalChunkDTO] = (
            DiversityService.diversify(
                reranked,
                top_k
            )
        )

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