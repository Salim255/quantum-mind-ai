import logging
import traceback
from fastapi import( FastAPI, Request, HTTPException)
from fastapi.responses import JSONResponse
from fastapi.exceptions import  RequestValidationError
from app.core.settings import Settings


logger = logging.getLogger(__name__)

class ExceptionsHandler:
    def __init__(self, app: FastAPI, settings: Settings):
        self.app = app
        self.settings = settings

    def register_handler(self):
        self.app.exception_handler(Exception)

    # =========================
    # GLOBAL EXCEPTION
    # =========================
    def global_exception_handler(
            self,
            request: Request,
            exc: Exception
            ):
        status_code: int = 500
        status: str = "error"
        message: str = "internal server error"

        body: dict = {
            "status": status,
            "message": message,
            "data": None,
        }

        if self.settings.is_dev:
            body["stack"] = "".join(
                traceback.format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__
                )
            )
        logger.exception(exc)
        return JSONResponse(
            status_code,
            data=body
        )
    
    # =========================
    # HTTP EXCEPTION
    # =========================
    async def http_global_handler(self):
        return ""
    
    # =========================
    # VALIDATION ERROR
    # =========================
    async def validation_handler(self):
        return ""