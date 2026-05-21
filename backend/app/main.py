import os
from app.core.settings import get_settings
from fastapi import FastAPI
from app.v1.modules.rag.services.implementations.loader_service_impl import LoaderServiceImpl
from app.v1.modules.rag.services.interfaces.loader_service import LoaderService
from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.conversation.controller.controller import router as conversation_router
from app.core.cors import setup_cors
from app.core.exceptions.global_exception_handler import ExceptionsHandler

def get_loader_service() -> LoaderService:
    return LoaderServiceImpl()
    
app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=get_settings().API_PREFIX
)

setup_cors(app)

app.include_router(conversation_router)
app.include_router(rag_router)

ExceptionsHandler(app, settings=get_settings)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}
