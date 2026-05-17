from ast import List
from app.ai_core.rag.services.interfaces.retriever_service import RetrieverService
from app.ai_core.rag.vector_store.search import search_similar_documents
from app.ai_core.structured_outputs.schemas.retrieval_result_schema import RetrievalResultSchema


class RetrieverServiceImpl(RetrieverService):
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