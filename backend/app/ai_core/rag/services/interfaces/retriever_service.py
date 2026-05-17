
from abc import ABC, abstractmethod

from app.ai_core.structured_outputs.schemas.rag_eval_schema import RetrievedChunk
from app.ai_core.structured_outputs.schemas.retrieval_result_schema import RetrievalResultSchema


# ------------------------------------------------------------------
# ABSTRACT RETRIEVER SERVICE INTERFACE
# ------------------------------------------------------------------
# Helper class that provides a standard way to create an ABC using
# inheritance and abstract methods.
# This is useful for defining a clear interface for the Retriever component
# in your RAG pipeline, without tying it to a specific implementation.
# ------------------------------------------------------------------
class RetrieverService(ABC):
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