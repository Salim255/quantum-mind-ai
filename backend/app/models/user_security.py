from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class UserSecurity(SQLModel, table=True):
    """
    Security state associated with a user.

    Keeps authentication protection concerns separate
    from the core User entity.

    Refresh tokens are intentionally NOT stored here.
    They belong to UserSession.
    """

    __tablename__ = "user_security"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )
    """
    Unique identifier of the security record.
    """

    user_id: UUID = Field(
        nullable=False,
        unique=True,
        foreign_key="users.id",
        index=True,
    )
    """
    User owning this security record.

    UNIQUE guarantees a one-to-one relationship.
    """

    # ============================================================
    # EMAIL SECURITY
    # ============================================================

    email_verified: bool = Field(
        default=False,
        nullable=False,
        index=True,
    )
    """
    Whether the user has verified ownership of the email address.
    """

    email_verified_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp when email verification succeeded.
    """

    # ============================================================
    # LOGIN PROTECTION
    # ============================================================

    failed_login_attempts: int = Field(
        default=0,
        nullable=False,
    )
    """
    Number of consecutive failed login attempts.

    Used for brute-force protection and account lockout.
    """

    locked_until: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp until which authentication is temporarily blocked.

    NULL means the account is not currently locked.
    """

    last_failed_login_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp of the most recent failed login attempt.
    """

    last_login_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp of the most recent successful login.
    """

    # ============================================================
    # PASSWORD SECURITY
    # ============================================================

    password_changed_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp of the most recent password change.

    Can be used to invalidate sessions created before
    the password was changed.
    """

    # ============================================================
    # SESSION INVALIDATION
    # ============================================================

    security_version: int = Field(
        default=0,
        nullable=False,
    )
    """
    Global security version for the account.

    Incrementing this value can invalidate all existing
    authentication sessions.

    Examples:

    - Password reset
    - Password compromise
    - Logout from all devices
    - Suspicious activity
    """

    # ============================================================
    # MULTI-FACTOR AUTHENTICATION
    # ============================================================

    mfa_enabled: bool = Field(
        default=False,
        nullable=False,
    )
    """
    Indicates whether MFA is enabled.

    MFA secrets should be stored separately in a dedicated
    credential table when MFA is implemented.
    """

    # ============================================================
    # ACCOUNT RISK
    # ============================================================

    compromised_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp when the account was identified as compromised.

    NULL means no compromise has been recorded.
    """

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    Timestamp when the security record was created.
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    Timestamp of the last security-state modification.
    """

    # ============================================================
    # RELATIONSHIP
    # ============================================================

    user: User = Relationship(
        back_populates="security",
    )
    """
    User associated with this security record.
    """
