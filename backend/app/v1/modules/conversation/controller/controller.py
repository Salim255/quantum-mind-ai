from fastapi import APIRouter, Depends
from typing import Annotated
from app.v1.modules.conversation.dependencies import get_conversation_service
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.conversation.schema.conversation_schema import ConversationResponse

router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)

@router.post("/messages")
async def send_message(
    conversation_service: Annotated[ConversationService, Depends(get_conversation_service)]
) -> ConversationResponse:
    rag_json = await conversation_service.handle_message("conversation_id", "Hello, quantum works?")
    return ConversationResponse(answer=rag_json)
