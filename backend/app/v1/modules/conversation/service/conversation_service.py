from abc import ABC, abstractmethod
from typing import Optional
from app.v1.modules.conversation.schema.conversation_schema import ConversationResponse

class ConversationService(ABC):
    
    @abstractmethod
    async def stream_message(
        self,
        user_id: str, 
        message: str, 
        conversation_id: Optional[str] = None
        ):
        pass
    
    @abstractmethod
    async def handle_message(
        self,
        user_id: str, 
        message: str, 
        conversation_id: Optional[str] = None
        ) -> ConversationResponse:
        # Placeholder for actual message processing logic
        pass