from fastapi import FastAPI

from app.v1.modules.rag.controller.controller import router as rag_router
from app.v1.modules.conversation.controller.controller import (
    router as conversation_router,
)
from app.v1.modules.learn.controller.controller import router as learn_router

class RouterService:
    @staticmethod
    def register_routers(app: FastAPI) -> None:
        """
        Register all application routers.
        """

        app.include_router(learn_router)
        app.include_router(conversation_router)
        app.include_router(rag_router)