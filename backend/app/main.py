from functools import lru_cache
import os
from app.core.settings import Settings
from fastapi import FastAPI, Depends, File, UploadFile
from typing import Annotated
from app.ai_core.llms.groq_llm import groq_llm_call, get_groq_client
from app.ai_core.rag.loader.ingest import ingest_pdf
import aiofiles   # Async file I/O library (non-blocking)
import uuid       # Generates unique filenames

@lru_cache
def get_settings():
    return Settings()

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=get_settings().API_PREFIX
)



@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}

@app.post("/rag/query")
def rag_query(query: str):
    # This is a placeholder for your RAG query endpoint.
    # It will eventually:
    # 1. Embed the query
    # 2. Search VECTOR_DB for relevant chunks
    # 3. Use retrieved chunks as context for an LLM response
    return {"query": query, "results": []}

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
async def ingest_pdf_endpoint(file: Annotated[UploadFile, File(...)]):
    """
    Receive a PDF file from the client (Postman, UI, etc.),
    save it asynchronously, then ingest it into the vector store.

    Parameters
    ----------
    file : UploadFile
        The uploaded PDF file sent by the client.

    Returns
    -------
    dict
        A JSON response confirming ingestion and showing how many chunks were added.
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
  
    result = ingest_pdf(temp_path)


    # -----------------------------------------------------------------------
    # 4. Return a clean JSON response
    # -----------------------------------------------------------------------
    # This tells the client:
    # - ingestion succeeded
    # - how many chunks were added
    # - what the original filename was

    print(f"Processing file : {temp_path}", result)  # Debug log to confirm file content (first 100 bytes)
    return {
        "status": "ok",
        "chunks_added": result["chunks_added"],
        "filename": file.filename
    }


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

    result = groq_llm_call(client, prompt, debug=True)

    ingest_pdf("my_first_quantum_lesson.pdf")

    return {
        "success": True,
        "llm_response": result
    }
