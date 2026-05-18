from abc import ABC, abstractmethod

from backend.app.ai_core.structured_outputs.schemas.retrieval_result_schema import RetrievalResultSchema

class RAGPipelineService(ABC):
    @abstractmethod
    def retrieve(self, query: str) -> RetrievalResultSchema:
        """
        Abstract method to retrieve relevant chunks of information based on the input query.

        Parameters
        ----------
        query : str
            The natural language question or query for which relevant information is to be retrieved.

        Returns
        -------
        RetrievalResultSchema
            The structured retrieval results containing the retrieved chunks and their associated sources.
        """
        pass