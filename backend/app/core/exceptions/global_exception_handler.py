import logging
import traceback
from fastapi import(FastAPI, Request)
from fastapi.responses import JSONResponse
from fastapi.exceptions import  RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.settings import Settings
from app.core.exceptions.base_exception import AppException

logger = logging.getLogger(__name__)

class ExceptionsHandler:
    def __init__(self, app: FastAPI, settings: Settings):
        self.app = app
        self.settings = settings
        self.register_handler()

    def register_handler(self):
        self.app.add_exception_handler(
            AppException,
            self.app_exception_handler
        )
        self.app.add_exception_handler(Exception, self.exception_handler)

        self.app.add_exception_handler(StarletteHTTPException, self.http_global_handler)

        self.app.add_exception_handler(RequestValidationError, self.validation_handler)

    # =========================
    # GLOBAL EXCEPTION
    # =========================
    def exception_handler(
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
            status_code=status_code,
            content=body
        )
    
    # =========================
    # HTTP EXCEPTION
    # =========================
    def http_global_handler(self, request: Request, exc: StarletteHTTPException):
        status = "error"

        body: dict = {
            "status": status,
            "message": str(exc.detail),
            "data": None
        }

        if self.settings.is_dev:
            body["stack"] = "".join(
                traceback.format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__
                )
            )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=body
        )
    
    # =========================
    # VALIDATION ERROR
    # =========================
    def validation_handler(self, request: Request, exc: RequestValidationError):
        status: str = "error"
        message: str = "Validation error"
        body: dict = {
            "status": status,
            "message": message,
            "data": exc.errors()
        }

        if self.settings.is_dev:
            body["stack"] = "".join(
                traceback.format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__
                )
            )
        return JSONResponse(
            status_code=422,
            content=body
        )
    
    def app_exception_handler(
        self,
        request: Request,
        exc: AppException
    ):

        body = {
            "status": "error",
            "error": exc.error_code,
            "message": exc.message,
            "data": exc.data
        }

        if self.settings.is_dev:
            body["stack"] = "".join(
                traceback.format_exception(
                    type(exc),
                    exc,
                    exc.__traceback__
                )
            )

        return JSONResponse(
            status_code=exc.status_code,
            content=body
        )