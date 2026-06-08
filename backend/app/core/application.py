import logging
from fastapi import FastAPI
from app.core.cors import setup_cors
from app.core.exceptions.global_exception_handler import ExceptionsHandler
from app.core.lifespan import lifespan
from app.core.router_registry import RouterService
from app.core.container import Container
from app.core.health import register_health_check

class ApplicationService:
    def __init__(self):
        # --------------------------------------------------------
        # CREATE SINGLE CONTAINER INSTANCE (ONCE)
        # --------------------------------------------------------  
        self.container = Container()

    @classmethod
    def create_app(cls) -> FastAPI:
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
            root_path=cls.container.settings.API_PREFIX,
        )

        # Make DI container available everywhere
        app.state.container = cls.container

        setup_cors(app)

        RouterService.register_routers(app)

        ExceptionsHandler(app, settings=cls.container.settings)

        register_health_check(app)

        return app