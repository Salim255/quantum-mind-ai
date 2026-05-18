from fastapi import (APIRouter, Depends)
from typing import Annotated

from pydantic import BaseModel
from app.ai_core.structured_outputs.schemas.rag_response_schema import RAGQueryResponseSchema
from app.ai_core.structured_outputs.schemas.rag_eval_schema import RAGEvaluationLog, RetrievedChunk
from app.v1.modules.rag.services.interfaces.rag_service import RAGService
from app.v1.modules.rag.dependencies import get_rag_service
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/query")
def rag_query(
    payload: QueryRequest,
    rag_service: Annotated[RAGService, Depends(get_rag_service)]
) -> RAGQueryResponseSchema:
    return rag_service.rag_pipeline(payload)

@router.post("/ingest/pdf")
# ---------------------------------------------------------------------------
# api/routes/ingest.py
# ---------------------------------------------------------------------------
# This endpoint allows you to upload a PDF (via Postman or UI)
# and ingest it into your QuantumMind AI vector database.
#
# It uses:
# - FastAPI's async request handling
# - aiofiles for non-blocking file writes
# - uuid4 for safe temporary filenames
#
# This is the modern, production-safe way to handle file uploads in 2026.
# ---------------------------------------------------------------------------
async def pdf_ingestion(
    file: Annotated[UploadFile, File(...)],
    loader_service: Annotated[LoaderService, Depends(get_loader_service)]
    ) -> IngestionResponseSchema:
    """
    Receive a PDF file from the client (Postman, UI, etc.),
    save it asynchronously, then ingest it into the vector store.

    Parameters
    ----------
    file : UploadFile
        The uploaded PDF file sent by the client.

    Returns
    -------
    IngestionResponseSchema
        A structured response confirming ingestion and showing how many chunks were added.
    """

    # -----------------------------------------------------------------------
    # 1. Generate a unique temporary filename
    # -----------------------------------------------------------------------
    # uuid4() ensures no filename collisions, even with concurrent uploads.
    # /tmp is the correct directory for temporary files in containers.
    temp_filename = f"{uuid.uuid4()}.pdf"
    temp_path = os.path.join("/tmp", temp_filename)

  
    # -----------------------------------------------------------------------
    # 2. Save the uploaded file asynchronously
    # -----------------------------------------------------------------------
    # aiofiles ensures we do NOT block the FastAPI event loop.
    # This is the modern, recommended way to handle file writes in async apps.
    async with aiofiles.open(temp_path, "wb") as out_file:
        # Read the uploaded file content asynchronously
        content = await file.read()
        # Write the content asynchronously to the temp file
        await out_file.write(content)


    # -----------------------------------------------------------------------
    # 3. Ingest the PDF into your vector database
    # -----------------------------------------------------------------------
    # ingest_pdf() handles:
    # - extracting text
    # - chunking
    # - embedding
    # - storing chunks in VECTOR_DB
  
    result = loader_service.ingest_pdf(temp_path, source=file.filename)


    # -----------------------------------------------------------------------
    # 4. Return a clean JSON response
    # -----------------------------------------------------------------------
    # This tells the client:
    # - ingestion succeeded
    # - how many chunks were added
    # - what the original filename was

    return result
