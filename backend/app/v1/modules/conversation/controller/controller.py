from fastapi import APIRouter, Depends
from typing import Annotated
from app.v1.modules.conversation.dependencies import get_conversation_service
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.conversation.schema.conversation_schema import ConversationRequest, ConversationResponse
from app.core.dtos.response_dto import ResponseDTO

router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)

@router.post("/messages")
async def send_message(
    payload: ConversationRequest,
    conversation_service: Annotated[ConversationService, Depends(get_conversation_service)]
) -> ResponseDTO:
    response: ConversationResponse = await conversation_service.handle_message(
        user_id=payload.user_id,
        message=payload.message,
        conversation_id=payload.conversation_id
    )
    return ResponseDTO(data=response)
