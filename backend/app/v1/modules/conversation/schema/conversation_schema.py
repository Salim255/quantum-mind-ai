from pydantic import BaseModel
from typing import Literal
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema

class MemoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    timestamp: float

class ConversationSession(BaseModel):
    user_id: str
    messages: list[MemoryMessage] = []

class ConversationRequest(BaseModel):
    message: str
    user_id: str  # or session_id

class ConversationResponse(BaseModel):
    answer: str
    memory_updated: bool = True

class ConversationResponse(BaseModel):
    answer: RAGQueryResponseSchema
    memory_updated: bool = True
