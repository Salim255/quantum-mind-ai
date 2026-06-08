from fastapi import FastAPI


def register_health_check(app: FastAPI) -> None:
    """
    Register health endpoints.
    """

    @app.get("/health")
    def health_check():
        return {
            "status": "ok",
            "message": "QuantumMind AI backend is running",
        }