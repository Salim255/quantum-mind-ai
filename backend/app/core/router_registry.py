from fastapi import FastAPI
from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.ingestion.controller.controller import router as ingestion_router
from app.v1.modules.quiz.controller.controller import router as quiz_router
from app.v1.modules.topic.controller.controller import topic_router
from app.v1.modules.section.controller.controller import section_router

class RouterService:
    @staticmethod
    def register_routers(app: FastAPI) -> None:
        """
        Register all application routers.
        """
        app.include_router(quiz_router)
        app.include_router(ingestion_router)
        app.include_router(rag_router)
        app.include_router(topic_router)
        app.include_router(section_router)