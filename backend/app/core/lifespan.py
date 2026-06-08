from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from app.core.application import container

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    """

    logger.info("Starting up QuantumMind AI backend... ✅")

    await container.qdrant.create_collection()

    container.db_init_service.create_tables()

    yield

    logger.info("Shutting down QuantumMind AI backend...")

    await container.qdrant.close()