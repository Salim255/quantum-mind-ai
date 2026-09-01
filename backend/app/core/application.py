import logging

from fastapi import FastAPI

from app.core.config.cors import setup_cors
from app.core.container import Container
from app.core.exceptions.global_exception_handler import ExceptionsHandler
from app.core.health import register_health_check
from app.core.lifespan import LifespanService
from app.core.router_registry import RouterService


class ApplicationService:
    """
    Responsible for creating and configuring the FastAPI
    application.

    ApplicationService is the composition root of the application.

    This is where application-wide infrastructure is assembled,
    including:

    - dependency container
    - application lifespan
    - middleware
    - CORS
    - routers
    - exception handling
    - health checks

    Business services should not be created here unless they are
    application-wide infrastructure dependencies.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(self) -> None:
        """
        Creates the application container.

        The container is created exactly once and is shared by
        the application.
        """

        # --------------------------------------------------------
        # SINGLE APPLICATION CONTAINER
        # --------------------------------------------------------

        # The container owns application-wide infrastructure such
        # as settings and database session management.
        #
        # It is intentionally created only once.
        self.container = Container()

    # ============================================================
    # APPLICATION CREATION
    # ============================================================

    def create_app(self) -> FastAPI:
        """
        Creates and configures the FastAPI application.

        The application is assembled here before it starts
        receiving HTTP requests.
        """

        # --------------------------------------------------------
        # LOGGING
        # --------------------------------------------------------

        logging.basicConfig(
            level=logging.INFO,
            format=(
                "%(asctime)s - "
                "%(name)s - "
                "%(levelname)s - "
                "%(message)s"
            ),
        )

        # --------------------------------------------------------
        # APPLICATION LIFESPAN
        # --------------------------------------------------------

        lifespan_service = LifespanService(
            container=self.container,
        )

        # --------------------------------------------------------
        # FASTAPI APPLICATION
        # --------------------------------------------------------

        app = FastAPI(
            lifespan=lifespan_service.lifespan,
            title="QuantumMind AI - Python Core",
            description=(
                "AI Core for quantum research assistant "
                "(RAG, embeddings, vector search, quantum math)"
            ),
            version="0.1.0",
            root_path=self.container.settings.API_PREFIX,
        )

        # ========================================================
        # APPLICATION STATE
        # ========================================================

        # Store the application container inside FastAPI state.
        #
        # This allows request-scoped dependencies to access the
        # same application container through:
        #
        #     request.app.state.container
        #
        # The container itself remains application-wide.
        app.state.container = self.container

        # ========================================================
        # CORS
        # ========================================================

        # Configure Cross-Origin Resource Sharing.
        #
        # This controls which frontend origins are allowed to
        # communicate with the API.
        setup_cors(app)

        # ========================================================
        # ROUTERS
        # ========================================================

        # Register all application routers.
        #
        # Authentication middleware is already registered globally,
        # so every registered endpoint automatically passes through
        # the authentication layer.
        RouterService.register_routers(app)

        # ========================================================
        # GLOBAL EXCEPTION HANDLING
        # ========================================================

        # Register centralized application exception handling.
        #
        # This converts application exceptions into consistent
        # HTTP responses.
        ExceptionsHandler(
            app,
            settings=self.container.settings,
        )

        # ========================================================
        # HEALTH CHECK
        # ========================================================

        # Register the application health endpoint.
        register_health_check(app)

        # --------------------------------------------------------
        # RETURN CONFIGURED APPLICATION
        # --------------------------------------------------------

        return app