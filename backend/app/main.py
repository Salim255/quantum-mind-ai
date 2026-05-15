from functools import lru_cache
import os

from pydantic import BaseModel
from app.core.settings import Settings
from fastapi import FastAPI, Depends, File, UploadFile
from typing import Annotated
from app.ai_core.llms.groq_llm import get_groq_client, groq_llm_call
from app.ai_core.rag.loader.ingest import ingest_pdf
import aiofiles   # Async file I/O library (non-blocking)
import uuid       # Generates unique filenames
from app.ai_core.rag.vector_store.search import search_similar_documents
from app.ai_core.rag.generator.llm_generator import generate_answer
from app.ai_core.rag.context.context_builder import build_context
from app.ai_core.rag.generator.answer_normalizer import normalize_final_answer

@lru_cache
def get_settings():
    return Settings()

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=get_settings().API_PREFIX
)


class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}

@app.post("/rag/query")
def rag_query(payload: QueryRequest, settings: Annotated[Settings, Depends(get_settings)]):
    """
    FULL RAG PIPELINE:
    1. Retrieve + rerank chunks
    2. Extract top chunks
    3. Build prompt + call LLM
    4. Return final answer
    """

    # --- 1. Retrieve + rerank chunks ----------------------------------------
    # search_similar_documents returns:
    # { "results": [chunk1, chunk2, chunk3] }
    retrieval_output = search_similar_documents(payload.query, payload.top_k)

    # Extract the list of text chunks
    chunks = retrieval_output["results"]

    # Build a rich context string for the LLM (optional, but improves answers)
    rich_context_chunks = build_context(chunks, max_chars=3000)

    # Take only the top 3 chunks for the LLM context
    

    # --- 2. Generate final answer using the LLM ------------------------------
    # This uses your RAGPromptBuilder internally
    client = get_groq_client(settings)
    final_answer = generate_answer(payload.query,  rich_context_chunks, client)
    normalize_answer =  normalize_final_answer(final_answer)
    # --- 3. Return everything to the client ---------------------------------
    return {
        "query": payload.query,
        "retrieved_chunks": rich_context_chunks,
        "final_answer": normalize_answer,
        "source": retrieval_output.get("sources", [])  # Include sources if available
    }

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
  
    result = ingest_pdf(temp_path, source=file.filename)


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
        "source": file.filename
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

    result = groq_llm_call(client, prompt)

    
    return {
        "success": True,
        "llm_response": result
    }
