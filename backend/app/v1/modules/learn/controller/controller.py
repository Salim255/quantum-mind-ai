from fastapi import APIRouter
from app.v1.modules.learn.service.learn_service import LearnService

router = APIRouter(
    prefix="/learns",
    tags=["Learns"]
)

@router.get(
    "/:topic",
    status_code=200
)
async def get_learn_topic(
    learn_service: LearnService
):
    return  learn_service.create_topic()