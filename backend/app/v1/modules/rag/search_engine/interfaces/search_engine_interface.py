from app.v1.modules.rag.dto.retrieval_dto import RetrievalResponseDTO

class SearchEngineInterface:
    def search(self, query: str, top_k: int)-> RetrievalResponseDTO:
        """
        Contract for all search engine implementations.
        """
        raise NotImplemented