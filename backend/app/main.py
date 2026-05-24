from fastapi import FastAPI
from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.conversation.controller.controller import router as conversation_router
from app.core.cors import setup_cors
from app.core.exceptions.global_exception_handler import ExceptionsHandler
from app.core.container import Container


app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=Container.settings.API_PREFIX
)

setup_cors(app)

app.include_router(conversation_router)
app.include_router(rag_router)

ExceptionsHandler(app, settings=Container.settings)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}
