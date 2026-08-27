from enum import Enum

class ErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"

    INVALID_TOKEN = "INVALID_TOKEN"

    USER_NOT_FOUND = "USER_NOT_FOUND"

    CONVERSATION_NOT_FOUND = "CONVERSATION_NOT_FOUND"

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"

    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"

    ACCOUNT_INACTIVE = "ACCOUNT_INACTIVE"

    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"

    AUTHENTICATION_PROCESSING_ERROR = "AUTHENTICATION_PROCESSING_ERROR"