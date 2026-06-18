from fastapi import(APIRouter, Depends, File, UploadFile)
from typing import Annotated
from app.v1.modules.ingestion.dto.ingestion_dto import IngestionResponseDto
router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"]
)

@router.post("/")
async def ingest_pdf(
    file: Annotated[UploadFile, File(...)],
    loader_service: Annotated[LoaderService, Depends(get_loader_service)]
) -> IngestionResponseDto:
    return await loader_service.upload_and_ingest_pdf(file=file)