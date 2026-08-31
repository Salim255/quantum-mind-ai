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



# ============================================================
# PROCESSING ERROR
# ============================================================

class ProcessingException(AppException):
    """
    Raised when an unexpected error occurs while processing
    an application operation.

    This exception represents an internal server error that
    should be exposed to the client only through a safe,
    application-defined message.

    The original underlying exception must be logged internally
    and must never be exposed directly to the client.

    Domain-specific context is represented through ErrorCode.
    """

    def __init__(
        self,
        message: str = "An unexpected error occurred.",
        error_code: ErrorCode = ErrorCode.PROCESSING_ERROR,
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
        )


# ============================================================
# RESOURCE NOT FOUND
# ============================================================

class NotFoundException(AppException):
    """
    Raised when a requested resource cannot be found.

    The specific resource is identified through ErrorCode when
    a more precise application error needs to be returned.
    """

    def __init__(
        self,
        message: str = "Resource not found.",
        error_code: ErrorCode = ErrorCode.NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message,
            status_code=404,
            error_code=error_code,
        )


# ============================================================
# RESOURCE CONFLICT
# ============================================================

class ConflictException(AppException):
    """
    Raised when an operation conflicts with the current state
    of an existing resource.

    Typical examples include:

    - attempting to create an already existing resource
    - violating a uniqueness constraint
    - attempting an incompatible state transition
    """

    def __init__(
        self,
        message: str = "Resource conflict.",
        error_code: ErrorCode = ErrorCode.CONFLICT,
    ) -> None:
        super().__init__(
            message=message,
            status_code=409,
            error_code=error_code,
        )


    # ============================================================
    # UNAUTHORIZED
    # ============================================================

    class UnauthorizedException(AppException):
        """
        Raised when authentication is required but the request
        does not contain valid authentication credentials.

        Typical examples include:

        - missing access token
        - invalid access token
        - expired access token
        - malformed access token
        - invalid authentication credentials

        This exception represents an authentication failure.

        It does NOT represent an authorization failure.

        Authentication:
            "Who are you?"

        Authorization:
            "Are you allowed to do this?"
        """

        def __init__(
            self,
            message: str = "Authentication required.",
            error_code: ErrorCode = ErrorCode.UNAUTHORIZED,
        ) -> None:
            super().__init__(
                message=message,
                status_code=401,
                error_code=error_code,
            )