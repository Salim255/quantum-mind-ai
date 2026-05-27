from fastapi import APIRouter, Depends
from typing import Annotated
import json
from app.v1.modules.conversation.dependencies import get_conversation_service
from app.v1.modules.conversation.service.conversation_service import ConversationService
from app.v1.modules.conversation.schema.conversation_schema import ConversationRequest, ConversationResponse
from app.core.dtos.response_dto import ResponseDTO
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
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


@router.post("/messages/stream")
async def stream_message(
    payload: ConversationRequest,
    conversation_service: Annotated[
        ConversationService,
        Depends(get_conversation_service)
    ]
):
    # ------------------------------------------------------
    # STREAM EVENTS FROM SERVICE
    # ------------------------------------------------------
    event_generator = conversation_service.stream_message(
        user_id=payload.user_id,
        message=payload.message,
        conversation_id=payload.conversation_id
    )

    return StreamingResponse(
        event_generator,
        media_type="text/event-stream"
    )