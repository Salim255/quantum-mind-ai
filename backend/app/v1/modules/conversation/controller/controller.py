from fastapi import APIRouter, Depends
from typing import Annotated
from app.v1.modules.conversation.dependencies import get_conversation_service
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.conversation.schema.conversation_schema import ConversationRequest, ConversationResponse

router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)

@router.post("/messages")
async def send_message(
    payload: ConversationRequest,
    conversation_service: Annotated[ConversationService, Depends(get_conversation_service)]
) -> ConversationResponse:
    response = await conversation_service.handle_message(
        user_id=payload.user_id,
        message=payload.message,
        conversation_id=payload.conversation_id
    )
    return response
