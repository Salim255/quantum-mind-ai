from pydantic import BaseModel

class ConversationRequest(BaseModel):
    message: str
    user_id: str  # or session_id

class ConversationResponse(BaseModel):
    answer: str
    memory_updated: bool = True
