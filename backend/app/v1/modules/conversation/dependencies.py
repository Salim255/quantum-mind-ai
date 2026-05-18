from backend.app.v1.modules.conversation.service.conversation_imp_service import ConversationServiceImpl
from backend.app.v1.modules.conversation.service.conversation_service import ConversationService

def get_conversation_service() -> ConversationService:
    return ConversationServiceImpl()