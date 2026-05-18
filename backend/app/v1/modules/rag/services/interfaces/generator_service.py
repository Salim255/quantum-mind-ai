from typing import List
from groq import Groq
from abc import ABC, abstractmethod
from app.ai_core.structured_outputs.schemas.rag_schema import RAGResponseSchema

# Abstract Base Class for the Generator Service in the RAG pipeline.
# This defines the interface that any concrete implementation of the Generator Service must follow.
class GeneratorService(ABC):
    @abstractmethod
    def generate_answer(self,  query: str,chunks: List[str],client: Groq) -> RAGResponseSchema:
        """Generates a response based on the query and retrieved context."""
        pass