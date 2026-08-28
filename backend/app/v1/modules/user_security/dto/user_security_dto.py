from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserSecurityDTO(BaseModel):
    """
    Represents the security state associated with a user account.

    UserSecurityDTO is the application-level representation of
    persistent user security information.

    It contains only security-related account state required by
    application services.

    Authentication credentials, passwords, sessions, tokens and
    user profile information are intentionally excluded.

    This DTO must never expose sensitive credential material such as:

    - password
    - password_hash
    - access tokens
    - refresh tokens
    - session identifiers
    - MFA secrets
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        description="Unique identifier of the security record.",
    )

    user_id: UUID = Field(
        description="Unique identifier of the user associated with the security state.",
    )

    # ============================================================
    # EMAIL SECURITY
    # ============================================================

    email_verified: bool = Field(
        description="Indicates whether the user's email address has been verified.",
    )

    email_verified_at: datetime | None = Field(
        description="Timestamp when the user's email address was verified.",
    )

    # ============================================================
    # LOGIN PROTECTION
    # ============================================================

    failed_login_attempts: int = Field(
        description="Number of consecutive failed authentication attempts.",
    )

    locked_until: datetime | None = Field(
        description="Timestamp until which authentication is temporarily blocked.",
    )

    last_failed_login_at: datetime | None = Field(
        description="Timestamp of the user's most recent failed authentication attempt.",
    )

    last_login_at: datetime | None = Field(
        description="Timestamp of the user's most recent successful authentication.",
    )

    # ============================================================
    # PASSWORD SECURITY
    # ============================================================

    password_changed_at: datetime | None = Field(
        description="Timestamp of the user's most recent password change.",
    )

    # ============================================================
    # SESSION INVALIDATION
    # ============================================================

    security_version: int = Field(
        description="Global security version used to invalidate existing authentication sessions.",
    )

    # ============================================================
    # MULTI-FACTOR AUTHENTICATION
    # ============================================================

    mfa_enabled: bool = Field(
        description="Indicates whether multi-factor authentication is enabled.",
    )

    # ============================================================
    # ACCOUNT RISK
    # ============================================================

    compromised_at: datetime | None = Field(
        description="Timestamp when the account was identified as compromised.",
    )

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime = Field(
        description="Timestamp when the security record was created.",
    )

    updated_at: datetime = Field(
        description="Timestamp when the security state was last modified.",
    )