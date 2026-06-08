import logging

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core.exceptions.global_exception_handler import ExceptionsHandler
from app.core.lifespan import lifespan, container
from app.core.router_registry import register_routers

class ApplicationService:
    @staticmethod
    def create_app() -> FastAPI:
        """
        Creates and configures the FastAPI application.
        """

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )

        app = FastAPI(
            lifespan=lifespan,
            title="QuantumMind AI - Python Core",
            description=(
                "AI Core for quantum research assistant "
                "(RAG, embeddings, vector search, quantum math)"
            ),
            version="0.1.0",
            root_path=container.settings.API_PREFIX,
        )

        # Make DI container available everywhere
        app.state.container = container

        setup_cors(app)

        register_routers(app)

        ExceptionsHandler(app, settings=container.settings)

        register_health_check(app)

        return app