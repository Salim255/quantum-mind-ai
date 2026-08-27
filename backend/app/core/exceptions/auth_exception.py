from app.core.exceptions.base_exception import AppException
from app.core.exceptions.custom_exceptions import ConflictException
from app.core.exceptions.error_code import ErrorCode


# ============================================================
# AUTHENTICATION BASE EXCEPTION
# ============================================================

class AuthException(AppException):
    """
    Base exception for authentication-related errors.

    All authentication-specific exceptions inherit from this
    class.

    This provides a common abstraction for errors related to:

    - authentication
    - credentials
    - account access
    - authentication security
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
# INVALID CREDENTIALS
# ============================================================

class InvalidCredentialsException(AuthException):
    """
    Raised when the provided authentication credentials are
    invalid.

    A generic message is intentionally used so the API does not
    reveal whether the email exists or the password is incorrect.
    """

    def __init__(
        self,
        message: str = "Invalid email or password.",
        error_code: ErrorCode = ErrorCode.INVALID_CREDENTIALS,
    ) -> None:
        super().__init__(
            message=message,
            status_code=401,
            error_code=error_code,
        )


# ============================================================
# EMAIL ALREADY EXISTS
# ============================================================

class EmailAlreadyExistsException(ConflictException):
    """
    Raised when registration is attempted using an email address
    that already belongs to an existing account.
    """

    def __init__(
        self,
        message: str = "An account with this email already exists.",
        error_code: ErrorCode = ErrorCode.EMAIL_ALREADY_EXISTS,
    ) -> None:
        super().__init__(
            message=message,
            error_code=error_code,
        )


# ============================================================
# ACCOUNT INACTIVE
# ============================================================

class AccountInactiveException(AuthException):
    """
    Raised when authentication is attempted using an inactive
    account.

    An inactive account remains in the system but is not allowed
    to authenticate.
    """

    def __init__(
        self,
        message: str = "This account is inactive.",
        error_code: ErrorCode = ErrorCode.ACCOUNT_INACTIVE,
    ) -> None:
        super().__init__(
            message=message,
            status_code=403,
            error_code=error_code,
        )


# ============================================================
# ACCOUNT LOCKED
# ============================================================

class AccountLockedException(AuthException):
    """
    Raised when authentication is attempted while the account
    is temporarily locked.

    Account locking is typically triggered after repeated failed
    authentication attempts.
    """

    def __init__(
        self,
        message: str = "This account is temporarily locked.",
        error_code: ErrorCode = ErrorCode.ACCOUNT_LOCKED,
    ) -> None:
        super().__init__(
            message=message,
            status_code=423,
            error_code=error_code,
        )