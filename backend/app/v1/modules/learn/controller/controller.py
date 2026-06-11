from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import Annotated
from app.v1.modules.learn.dependencies import (
    get_doc_ingestion_service,
    get_learn_service,
    get_topic_ingestion_service,
    get_doc_ingestion_service_v2
    )
from app.v1.modules.learn.service.learn_service import LearnService
from app.v1.modules.learn.service.topic_ingestion_service import TopicIngestionService
from app.v1.modules.learn.dto.create_topic_dto import CreateTopicsFromPdfDTO
from app.v1.modules.learn.service.doc_ingestion_service import DocIngestionService
from app.v1.modules.learn.service.doc_ingestion_service_v2 import DocIngestionServiceV2

router = APIRouter(
    prefix="/learns",
    tags=["Learns"]
)

@router.post("/ingest-pdf")
async def upload_pdf_doc(
    file: Annotated[UploadFile, File(...)],
    doc_ingestion_service: Annotated[DocIngestionServiceV2, Depends(get_doc_ingestion_service_v2)]
):
    return doc_ingestion_service.pdf_ingestion_pipeline(file=file)

@router.post("/create-topics")
async def upload_pdf_topic(
    file: Annotated[UploadFile, File(...)],
    topics: Annotated[str, Form(...)],
    topic_ingestion_service: Annotated[TopicIngestionService, Depends(get_topic_ingestion_service)]
):  
    dto = CreateTopicsFromPdfDTO.model_validate_json(topics)
    
    return await topic_ingestion_service.create_topic_from_pdf(
        file=file,
        topics=dto,
    )

@router.get(
    "/topics",
    status_code=200
)
async def get_learn_topic(
    learn_service:  Annotated[LearnService, Depends(get_learn_service)]
):
    return  learn_service.get_topics()