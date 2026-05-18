from fastapi import APIRouter

rag_router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)

@rag_router.post("/query")
def query():
    return {"message": "RAG query endpoint"}