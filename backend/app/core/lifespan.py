from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.core.container import Container

logger = logging.getLogger(__name__)


class LifespanService:
    def __init__(self, container: Container):
        self.container = container

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        logger.info("Starting up QuantumMind AI backend... ✅")

        await self.container.qdrant.create_collection()

        self.container.db_init_service.create_tables()

        yield

        logger.info("Shutting down QuantumMind AI backend...")

        await self.container.qdrant.close()