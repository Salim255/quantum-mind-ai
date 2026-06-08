from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

@router.get(
    "/messages",
    status_code=200
)
async def get_learn_topic():
    return ""