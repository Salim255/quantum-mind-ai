from functools import lru_cache
from app.core.settings import Settings
from fastapi import FastAPI, Depends
from typing import Annotated
from app.ai_core.llms.groq_llm import groq_llm_call, get_groq_client

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0"
)

@lru_cache
def get_settings():
    return Settings()

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}

@app.get("/llm/test")
def test_llm(settings: Annotated[Settings, Depends(get_settings)]):
    prompt = """
    Generate a JSON object with:
    - greeting: a friendly message
    - status: 'connected'
    - model: the model name you are using
    """

    client = get_groq_client(settings)

    result = groq_llm_call(client, prompt, debug=True)

    return {
        "success": True,
        "llm_response": result
    }