from functools import lru_cache
import os
from app.core.settings import Settings, get_settings
from fastapi import FastAPI, Depends, File, UploadFile
from typing import Annotated
from app.ai_core.llms.groq_llm import get_groq_client, groq_llm_call
import aiofiles   # Async file I/O library (non-blocking)
import uuid       # Generates unique filenames
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
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
