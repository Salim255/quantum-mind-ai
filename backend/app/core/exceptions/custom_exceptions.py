from app.core.exceptions.base_exception import AppException
from app.core.exceptions.error_code import ErrorCode

class LoaderException(AppException):
    def __init__(
            self,
            message: str,
            error_code: ErrorCode
        ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code
        )
        
class StreamException(AppException):
    def __init__(
            self,
            message: str,
            error_code: ErrorCode
            ):
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code
        )

class NotFoundException(AppException):
    def __init__(
            self,
            message: str = "Resource not found",
            error_code: ErrorCode = ErrorCode.NOT_FOUND
            ):
        super().__init__(
            message=message,
            status_code=404,
            error_code=error_code
            )