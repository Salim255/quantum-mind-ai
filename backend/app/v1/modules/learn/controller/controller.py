from fastapi import APIRouter, UploadFile, File, Depends
from typing import Annotated
from app.v1.modules.learn.dependencies import get_learn_service, get_topic_ingestion_service
from app.v1.modules.learn.service.learn_service import LearnService
from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService


router = APIRouter(
    prefix="/learns",
    tags=["Learns"]
)

@router.post("/upload-pdf")
async def upload_pdf_topic(
    file: Annotated[UploadFile, File(...)],
    topic_ingestion_service: Annotated[TopicIngestionService, get_topic_ingestion_service]
):  
    return await topic_ingestion_service.create_topic_from_pdf(
        file=file,
        category=category,
    )

@router.get(
    "/topics",
    status_code=200
)
async def get_learn_topic(
    learn_service:  Annotated[LearnService, Depends(get_learn_service)]
):
    return  learn_service.get_topics()