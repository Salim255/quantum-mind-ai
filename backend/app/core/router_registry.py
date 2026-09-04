from fastapi import FastAPI
from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.ingestion.controller.controller import router as ingestion_router
from app.v1.modules.topic.controller.controller import topic_router
from app.v1.modules.section.controller.controller import section_router
from app.v1.modules.question.controller.controller import question_router
from app.v1.modules.answer.controller.controller import answer_router
from app.v1.modules.attempt.controller.controller import attempt_router
from app.v1.modules.auth.controller.controller import auth_router
from app.v1.modules.explore.controller.controller import  explore_router

class RouterService:
    @staticmethod
    def register_routers(app: FastAPI) -> None:
        """
        Register all application routers.
        """

        app.include_router(explore_router)
        app.include_router(auth_router)
        app.include_router(attempt_router)
        app.include_router(answer_router)
        app.include_router(question_router)
        app.include_router(ingestion_router)
        app.include_router(rag_router)
        app.include_router(topic_router)
        app.include_router(section_router)