from fastapi import Depends
from typing import Annotated
from app.v1.modules.conversation.service.conversation_imp_service import ConversationServiceImpl
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.conversation.memory.memory_manager import MemoryManager
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.rag.services.rag_service import RAGService

memory_manager = MemoryManager()

def get_memory_manager() -> MemoryManager:
    return memory_manager

def get_conversation_service(
        memory: Annotated[MemoryManager, Depends(get_memory_manager)],
        rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> ConversationService:
    return ConversationServiceImpl(memory=memory, rag_service=rag_service)


