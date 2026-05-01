from fastapi import FastAPI

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}