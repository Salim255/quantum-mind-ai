from app.core.exceptions.base_exception import AppException
from app.core.exceptions.error_code import ErrorCode


# ============================================================
# PROFILE BASE EXCEPTION
# ============================================================

class ProfileException(AppException):
    """
    Base exception for profile-related errors.

    All profile exceptions inherit from this class.

    This provides a common abstraction for errors related to:

    - profile creation
    - profile retrieval
    - profile data
    - profile processing
    """

    def __init__(
        self,
        message: str,
        status_code: int,
        error_code: ErrorCode,
    ) -> None:
        super().__init__(
            message=message,
            status_code=status_code,
            error_code=error_code,
        )


# ============================================================
# PROFILE ALREADY EXISTS
# ============================================================

class ProfileAlreadyExistsException(ProfileException):
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
            status_code=409,
            error_code=error_code,
        )


# ============================================================
# PROFILE NOT FOUND
# ============================================================

class ProfileNotFoundException(ProfileException):
    """
    Raised when a profile cannot be found for the requested user.

    This typically occurs when a profile is requested for a user
    who does not yet have an associated profile.
    """

    def __init__(
        self,
        message: str = "Profile not found.",
        error_code: ErrorCode = ErrorCode.PROFILE_NOT_FOUND,
    ) -> None:
        super().__init__(
            message=message,
            status_code=404,
            error_code=error_code,
        )


# ============================================================
# PROFILE PROCESSING ERROR
# ============================================================

class ProfileProcessingException(ProfileException):
    """
    Raised when an unexpected error occurs during a profile
    workflow.

    The original exception should be logged internally but
    must not be exposed to the client.
    """

    def __init__(
        self,
        message: str = (
            "An unexpected profile error occurred."
        ),
        error_code: ErrorCode = (
            ErrorCode.PROFILE_PROCESSING_ERROR
        ),
    ) -> None:
        super().__init__(
            message=message,
            status_code=500,
            error_code=error_code,
        )