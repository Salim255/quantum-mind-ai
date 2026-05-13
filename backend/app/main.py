from fastapi import FastAPI
from app.ai_core.llms.groq_llm import groq_llm_call

app = FastAPI(
    title="QuantumMind AI - Python Core",
    description="AI Core for quantum research assistant (RAG, embeddings, vector search, quantum math)",
    version="0.1.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "QuantumMind AI backend is running"}

@app.get("/llm/test")
def test_llm():
    prompt = """
    Generate a JSON object with:
    - greeting: a friendly message
    - status: 'connected'
    - model: the model name you are using
    """

    result = groq_llm_call(prompt, debug=True)

    return {
        "success": True,
        "llm_response": result
    }