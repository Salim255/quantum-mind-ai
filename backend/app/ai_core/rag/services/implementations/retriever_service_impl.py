from ast import List
from app.ai_core.rag.services.interfaces.retriever_service import RetrieverService
from app.ai_core.rag.vector_store.search import search_similar_documents
from app.ai_core.structured_outputs.schemas.rag_eval_schema import RetrievedChunk


class RetrieverServiceImpl(RetrieverService):
    def retrieve(self, query: str):
        """
        Retrieves relevant chunks of information based on the input query.

        Parameters
        ----------
        query : str
            The natural language question or query for which relevant information is to be retrieved.

        Returns
        -------
        List[RetrievedChunk]
            A list of retrieved chunks, where each chunk contains the text and its relevance score.
        """
        return search_similar_documents(query)