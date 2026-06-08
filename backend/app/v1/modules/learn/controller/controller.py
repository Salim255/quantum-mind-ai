from fastapi import APIRouter, Depends
from typing import Annotated
from app.v1.modules.learn.dependencies import get_learn_service
from app.v1.modules.learn.service.learn_service import LearnService

router = APIRouter(
    prefix="/learns",
    tags=["Learns"]
)

@router.get(
    "/topics",
    status_code=200
)
async def get_learn_topic(
    learn_service:  Annotated[LearnService, Depends(get_learn_service)]
):
    return  learn_service.get_topics()