from fastapi import APIRouter

router = APIRouter(
    prefix="/conversations",
    tags=["Conversation"]
)

@router.post("/")
def start_conversation():
    return {"message": "Conversation started"}