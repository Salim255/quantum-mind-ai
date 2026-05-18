from functools import lru_cache
import os
from app.core.settings import Settings, get_settings
from pydantic import BaseModel
from app.core.settings import Settings
from fastapi import FastAPI, Depends, File, UploadFile
from typing import Annotated
from app.ai_core.llms.groq_llm import get_groq_client, groq_llm_call
import aiofiles   # Async file I/O library (non-blocking)
import uuid       # Generates unique filenames
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.ai_core.structured_outputs.schemas.ingestion_schema import IngestionResponseSchema
from app.v1.modules.rag.controller.controller import router as rag_router

def get_loader_service() -> LoaderService:
    return LoaderServiceImpl()
    
app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=get_settings().API_PREFIX
)

app.include_router(rag_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}


@app.post("/ingest/pdf")
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
async def ingest_pdf_endpoint(
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


@app.get("/llm/test")
def test_llm(settings: Annotated[Settings, Depends(get_settings)]):
    prompt = """
    Generate a JSON object with:
    - greeting: a friendly message to my girlfriend her name is Pauline, tell her happy birthday, with nice message, lovely one 
    - status: 'connected'
    - model: the model name you are using
    - message: your message should go here
    """

    client = get_groq_client(settings)

    result = groq_llm_call(client, prompt)

    
    return {
        "success": True,
        "llm_response": result
    }
