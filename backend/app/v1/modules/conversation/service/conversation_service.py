from abc import ABC, abstractmethod
from app.ai_core.structured_outputs.schemas.rag_schema import RAGResponseSchema

class ConversationService(ABC):
    @abstractmethod
    async def handle_message(self, conversation_id: str, message: str)-> RAGResponseSchema:
        # Placeholder for actual message processing logic
        pass