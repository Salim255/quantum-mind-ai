import time
from typing import Dict, List

from app.v1.modules.conversation.dto.conversation_dto import ConversationSession, MemoryMessage

class MemoryManager:
    def __init__(self):
        self.sessions: Dict[str, ConversationSession] = {}

    def get_history(self, user_id: str) -> List[MemoryMessage]:
        session = self.sessions.get(user_id)
        if session:
            return session.messages
        return []

    def add_message(self, user_id: str, role: str, content: str):
        if user_id not in self.sessions:
            self.sessions[user_id] = ConversationSession(
                user_id=user_id,
                messages=[]
            )

        message = MemoryMessage(
            role=role,
            content=content,
            timestamp=time.time()
        )

        self.sessions[user_id].messages.append(message)
