from fastapi import (APIRouter, Depends)
from typing import Annotated, Generator
from pydantic import BaseModel
from app.v1.modules.rag.dto.rag_finale_response_dto import RAGQueryFinaleResponseDto
from app.v1.modules.rag.services.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.v1.modules.rag.dto.conversation_dto import (
    ConversationRequest,
    ConversationResponse)
from app.core.dtos.response_dto import ResponseDTO
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

async def send_message(
    payload: ConversationRequest,
    rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> ResponseDTO:
    response: ConversationResponse = await rag_service.handle_message(
        user_id=payload.user_id,
        message=payload.message,
        conversation_id=payload.conversation_id
    )
    return ResponseDTO(data=response)


@router.post(
    "/stream",
    status_code=200,
     response_class=StreamingResponse,
    response_description="Streams AI response chunks",
    responses={
        500: {"description": "Streaming failed"}
    }
)
async def stream_message(
    payload: ConversationRequest,
    rag_service: Annotated[
        RAGService,
        Depends(get_rag_service)
    ]
)-> StreamingResponse:
    # ------------------------------------------------------
    # STREAM EVENTS FROM SERVICE
    # ------------------------------------------------------
    event_generator: Generator[str, None, None] = rag_service.rag_stream_pipeline(
        QueryRequest(query=payload.message, top_k=3)
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