from fastapi import FastAPI
import logging
from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.conversation.controller.controller import router as conversation_router
from app.core.cors import setup_cors
from app.core.exceptions.global_exception_handler import ExceptionsHandler
from app.core.container import Container


# --------------------------------------------------------
# CREATE SINGLE CONTAINER INSTANCE (ONCE)
# --------------------------------------------------------
container = Container()

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0",
    root_path=container.settings.API_PREFIX
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

#@app.lifespan("startup")
#async def startup_event():
#   nltk.download("punkt", quiet=True)
# --------------------------------------------------------
# STORE IT INSIDE FASTAPI STATE
# --------------------------------------------------------
app.state.container = container

setup_cors(app)

app.include_router(conversation_router)
app.include_router(rag_router)

ExceptionsHandler(app, settings=container.settings)
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}
  
