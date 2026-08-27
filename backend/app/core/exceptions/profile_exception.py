from app.core.exceptions.error_code import ErrorCode
from app.core.exceptions.custom_exceptions import (
    ConflictException,
    NotFoundException,
)


# ============================================================
# PROFILE ALREADY EXISTS
# ============================================================

class ProfileAlreadyExistsException(ConflictException):
    """
    Raised when an attempt is made to create a profile for a user
    who already has an associated profile.

    Each user can have only one profile.
    """

    def __init__(
        self,
        message: str = "A profile already exists for this user.",
        error_code: ErrorCode = ErrorCode.PROFILE_ALREADY_EXISTS,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
        )


# ============================================================
# PROFILE NOT FOUND
# ============================================================

class ProfileNotFoundException(NotFoundException):
    """
    Raised when a requested profile cannot be found.
    """

    def __init__(
        self,
        message: str = "Profile not found.",
        error_code: ErrorCode = ErrorCode.PROFILE_NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
        )


# ============================================================
# PROFILE NOT FOUND
# ============================================================

class ProfileNotFoundException(NotFoundException):
    """
    Raised when a requested profile cannot be found.
    """

    def __init__(
        self,
        message: str = "Profile not found.",
        error_code: ErrorCode = ErrorCode.PROFILE_NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
        )