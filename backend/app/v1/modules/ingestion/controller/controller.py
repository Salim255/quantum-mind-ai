from fastapi import(APIRouter, Depends, File, UploadFile)
from typing import Annotated
from app.v1.modules.ingestion.dto.ingestion_dto import IngestionResponseDto
from app.v1.modules.ingestion.dependencies import DocIngestionService, get_doc_ingestion_service

router = APIRouter(
    prefix="/ingestions",
    tags=["Ingestion"]
)

@router.post("/ingest-pdf")
async def ingest_pdf(
    file: Annotated[UploadFile, File(...)],
    doc_ingestion_service: Annotated[DocIngestionService, Depends(get_doc_ingestion_service)]
):
    return await doc_ingestion_service.pdf_ingestion_pipeline(file=file)
 