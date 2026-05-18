from app.v1.modules.rag.services.interfaces.rag_pipeline_service import RAGPipelineService
from backend.app.ai_core.structured_outputs.schemas.retrieval_result_schema import RetrievalResultSchema
from backend.app.v1.modules.rag.vector_store.search import search_similar_documents

class RAGPipelineServiceImpl(RAGPipelineService):
     def retrieve(self, query: str)-> RetrievalResultSchema: 
        """
        Retrieves relevant chunks of information based on the input query.

        Parameters
        ----------
        query : str
            The natural language question or query for which relevant information is to be retrieved.

        Returns
        -------
        RetrievalResultSchema
            The structured retrieval results containing the retrieved chunks and their associated sources.
        """
        return search_similar_documents(query)