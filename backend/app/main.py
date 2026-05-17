from functools import lru_cache
import os
import time
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
from app.ai_core.structured_outputs.schemas.rag_eval_schema import (
    RAGEvaluationLog,
    RetrievedChunk
)
from app.ai_core.rag.evaluation.logger import (
    log_rag_evaluation
)
from app.ai_core.rag.services.implementations.retriever_service_impl import RetrieverServiceImpl

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
def rag_query(
    payload: QueryRequest,
    settings: Annotated[Settings, Depends(get_settings)]
):
    """
    Execute the full RAG pipeline.

    INPUT
    -----
    payload.query:
        User question

    payload.top_k:
        Number of chunks to retrieve

    OUTPUT
    ------
    - query
    - retrieved chunks
    - structured final answer
    - sources
    - latency
    """

    # ---------------------------------------------------------------
    # START LATENCY TIMER
    # ---------------------------------------------------------------
    #
    # We measure total pipeline execution time.
    #
    # Useful later for:
    # - monitoring
    # - dashboard analytics
    # - optimization
    # - performance regression detection
    # ---------------------------------------------------------------
    start_time = time.perf_counter()

    # ---------------------------------------------------------------
    # 1. SEMANTIC RETRIEVAL + RERANKING
    # ---------------------------------------------------------------
    #
    # search_similar_documents():
    #
    # - embeds the query
    # - performs cosine similarity search
    # - selects top candidates
    # - reranks using cross-encoder
    #
    # RETURNS:
    # {
    #   "results": [...],
    #   "sources": [...]
    # }
    # ---------------------------------------------------------------
    retriever = RetrieverServiceImpl()
    retrieval_output = retriever.retrieve(payload.query)

    print("[DEBUG] Retrieval output:", retrieval_output)  # Debug log to inspect retrieval results
    # ---------------------------------------------------------------
    # EXTRACT RETRIEVED CHUNKS
    # ---------------------------------------------------------------
    chunks = retrieval_output["results"]

    # ---------------------------------------------------------------
    # EXTRACT SOURCES
    # ---------------------------------------------------------------
    #
    # Sources help:
    # - explain provenance
    # - improve trust
    # - support evaluation
    # ---------------------------------------------------------------
    sources = retrieval_output.get("sources", [])

    # ---------------------------------------------------------------
    # 2. BUILD OPTIMIZED CONTEXT
    # ---------------------------------------------------------------
    #
    # build_context():
    #
    # - merges top chunks
    # - limits total context size
    # - preserves semantic coherence
    #
    # WHY IMPORTANT?
    # --------------
    # LLMs perform better with:
    # - focused context
    # - low noise
    # - coherent passages
    # ---------------------------------------------------------------
    rich_context_chunks = build_context(
        chunks,
        max_chars=3000
    )

    # ---------------------------------------------------------------
    # 3. INITIALIZE LLM CLIENT
    # ---------------------------------------------------------------
    #
    # This creates the Groq client using API keys
    # from application settings.
    # ---------------------------------------------------------------
    client = get_groq_client(settings)

    # ---------------------------------------------------------------
    # 4. GENERATE FINAL STRUCTURED ANSWER
    # ---------------------------------------------------------------
    #
    # generate_answer():
    #
    # - builds the final RAG prompt
    # - injects context
    # - calls the LLM
    # - validates structured JSON output
    #
    # RETURNS:
    # RAGResponseSchema
    # ---------------------------------------------------------------
    final_answer = generate_answer(
        payload.query,
        rich_context_chunks,
        client
    )

    # ---------------------------------------------------------------
    # STOP LATENCY TIMER
    # ---------------------------------------------------------------
    #
    # Convert total execution time into milliseconds.
    # ---------------------------------------------------------------
    latency_ms = (
        time.perf_counter() - start_time
    ) * 1000

    # ---------------------------------------------------------------
    # 5. BUILD STRUCTURED RETRIEVED CHUNKS
    # ---------------------------------------------------------------
    #
    # We transform raw chunks into structured objects
    # for evaluation logging.
    #
    # WHY?
    # ----
    # Later we can:
    # - inspect retrieval quality
    # - build dashboards
    # - compute metrics
    # - analyze hallucinations
    # ---------------------------------------------------------------
    retrieved_chunk_objects = []

    for chunk, source in zip(chunks, sources):

        retrieved_chunk_objects.append(

            RetrievedChunk(
                text=chunk,
                source=source
            )
        )

    # ---------------------------------------------------------------
    # 6. CREATE RAG EVALUATION LOG
    # ---------------------------------------------------------------
    #
    # This stores:
    # - query
    # - retrieved chunks
    # - final answer
    # - latency
    # - model info
    #
    # This becomes the foundation of:
    # - RAG analytics
    # - evaluation dashboards
    # - retrieval benchmarking
    # ---------------------------------------------------------------
    evaluation_log = RAGEvaluationLog(

        query=payload.query,

        retrieved_chunks=retrieved_chunk_objects,

        final_answer=final_answer.model_dump(),

        latency_ms=latency_ms,

        model="llama-3.1-8b-instant",

        top_k=payload.top_k
    )

    # ---------------------------------------------------------------
    # 7. SAVE EVALUATION LOG
    # ---------------------------------------------------------------
    #
    # Logs are stored in JSONL format.
    #
    # Every request becomes:
    # - traceable
    # - measurable
    # - debuggable
    # ---------------------------------------------------------------
    log_rag_evaluation(evaluation_log)

    # ---------------------------------------------------------------
    # 8. RETURN API RESPONSE
    # ---------------------------------------------------------------
    #
    # model_dump():
    # Converts Pydantic schema into JSON-serializable dict.
    # ---------------------------------------------------------------
    return {

        "query": payload.query,

        "retrieved_chunks": rich_context_chunks,

        "final_answer": final_answer.model_dump(),

        "source": sources,

        "latency_ms": latency_ms
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
