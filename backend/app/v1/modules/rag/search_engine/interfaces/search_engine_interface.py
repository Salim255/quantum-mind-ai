from app.v1.modules.rag.dto.retrieval_dto import RetrievalResponseDTO
from abc import ABC, abstractmethod

class SearchEngineInterface(ABC):
    @abstractmethod
    def search_similar_documents(
            self,
            query: str,
            top_k: int
            )-> RetrievalResponseDTO:
        """
        Contract for all search engine implementations.
        """
        pass