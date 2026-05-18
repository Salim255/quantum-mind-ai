from fastapi import APIRouter

router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)

@router.post("/messages")
def send_message():
    return {"message": "Message sent to conversation endpoint"}