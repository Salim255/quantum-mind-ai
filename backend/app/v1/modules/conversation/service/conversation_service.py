from abc import ABC, abstractmethod

class ConversationService(ABC):
    @abstractmethod
    def send_message(self, conversation_id: str, message: str):
        # Placeholder for actual message processing logic
        pass