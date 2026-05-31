from abc import ABC, abstractmethod
from typing import Optional, AsyncGenerator
from app.v1.modules.conversation.dto.conversation_dto import ConversationResponse

class ConversationService(ABC):
    
    @abstractmethod
    def stream_message(
        self,
        user_id: str, 
        message: str, 
        conversation_id: Optional[str] = None
        )-> AsyncGenerator[str, None]:
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