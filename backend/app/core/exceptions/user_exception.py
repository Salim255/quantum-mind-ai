from app.core.exceptions.custom_exceptions import NotFoundException
from app.core.exceptions.error_code import ErrorCode


# ============================================================
# USER NOT FOUND
# ============================================================

class UserNotFoundException(NotFoundException):
    """
    Raised when a requested user cannot be found.
    """

    def __init__(
        self,
        message: str = "User not found.",
        error_code: ErrorCode = ErrorCode.USER_NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
        )