from fastapi import (APIRouter, Depends)
from typing import Annotated
from pydantic import BaseModel
from app.v1.modules.rag.dto.rag_finale_response_dto import RAGQueryFinaleResponseDto
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.rag.dto.conversation_dto import (ConversationRequest, ConversationResponse)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

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


@router.post(
    "/messages/stream",
    status_code=200,
     response_class=StreamingResponse,
    response_description="Streams AI response chunks",
    responses={
        500: {"description": "Streaming failed"}
    }
)
async def stream_message(
    payload: ConversationRequest,
    conversation_service: Annotated[
        ConversationService,
        Depends(get_conversation_service)
    ]
)-> StreamingResponse:
    # ------------------------------------------------------
    # STREAM EVENTS FROM SERVICE
    # ------------------------------------------------------
    event_generator: Generator[str, None, None] = conversation_service.stream_message(
        user_id=payload.user_id,
        message=payload.message,
        conversation_id=payload.conversation_id
    )

    return StreamingResponse(
        event_generator,
        media_type="text/event-stream"
        )

@router.post("/query")
def rag_query(
    payload: QueryRequest,
    rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> RAGQueryFinaleResponseDto:
    return rag_service.rag_pipeline(payload)