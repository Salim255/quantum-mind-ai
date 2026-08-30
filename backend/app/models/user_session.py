from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class UserSession(SQLModel, table=True):
    """
    Represents an authenticated user session.

    A user can have multiple sessions at the same time:

        User
        ├── Mac / Chrome
        ├── iPhone
        └── Other browser

    This table manages the lifecycle of refresh-token based
    authentication sessions.

    IMPORTANT:

    The raw refresh token is NEVER stored in the database.

    Instead, the authentication service stores a cryptographic
    hash of the refresh token and compares hashes when a token
    is presented.

    Access tokens remain short-lived and are not persisted here.

    UserSession is responsible for:

    - refresh-token rotation
    - session expiration
    - session revocation
    - device/session identification
    - security-version validation
    - login/logout auditing
    """

    __tablename__ = "user_sessions"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )
    """
    Unique identifier of the authentication session.

    This ID is safe to expose internally as a session identifier
    because it is not the refresh token itself.
    """

    user_id: UUID = Field(
        nullable=False,
        index=True,
        foreign_key="users.id",
    )
    """
    User who owns this authentication session.

    A user may have many sessions.

        User 1 ───────── N UserSession
    """

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    refresh_token_hash: str | None = Field(
        nullable=True,
        unique=True,
        index=True,
        max_length=255,
    )
    """
    Cryptographic hash of the current refresh token.

    NEVER store the raw refresh token.

    Authentication flow:

        Client
          │
          │ refresh_token
          ▼
        API
          │
          │ hash(token)
          ▼
        refresh_token_hash
          │
          ▼
        database comparison

    A hash allows the database to remain useless to an attacker
    who obtains the stored session records.

    The hash should be generated using a cryptographically secure
    mechanism appropriate for token verification.
    """

    # ============================================================
    # TOKEN ROTATION
    # ============================================================

    token_version: int = Field(
        default=1,
        nullable=False,
    )
    """
    Version of the refresh token currently associated with
    this session.

    Incremented whenever the refresh token is rotated.

    Example:

        token_version = 1

        refresh request

        token_version = 2

    This makes token rotation explicit and helps detect replay
    of previously issued refresh tokens.
    """

    previous_token_hash: str | None = Field(
        default=None,
        max_length=255,
    )
    """
    Hash of the immediately previous refresh token.

    Used for refresh-token rotation and replay detection.

    Once a refresh token has been rotated, presentation of the
    previous token can indicate token reuse.

    Depending on the security policy, token reuse should normally
    revoke the entire session.
    """

    # ============================================================
    # SESSION LIFECYCLE
    # ============================================================

    expires_at: datetime | None = Field(
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    UTC timestamp when the session expires.

    After this timestamp the refresh token must no longer be
    accepted.

    This provides an absolute lifetime for the session.
    """

    last_used_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    UTC timestamp when this session was last successfully used.

    Updated when the refresh token is successfully exchanged
    for a new access/refresh token pair.
    """

    revoked_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    UTC timestamp when the session was revoked.

    NULL means the session has not been explicitly revoked.

    A revoked session must never be accepted for token refresh.

    Revocation can happen because of:

    - user logout
    - logout from all devices
    - password reset
    - account compromise
    - refresh-token reuse
    - administrator action
    """

    # ============================================================
    # SECURITY VERSION
    # ============================================================

    security_version: int = Field(
        default=0,
        nullable=False,
    )
    """
    Security version captured when the session was created.

    It must match UserSecurity.security_version.

    Example:

        UserSecurity.security_version = 4

        New session:
            security_version = 4

        Password reset:
            UserSecurity.security_version = 5

    Existing sessions containing version 4 become invalid.

    This allows global session invalidation without having to
    individually revoke every session.
    """

    # ============================================================
    # DEVICE / CLIENT INFORMATION
    # ============================================================

    device_name: str | None = Field(
        default=None,
        max_length=255,
    )
    """
    Human-readable device/session name.

    Examples:

        MacBook Pro
        iPhone
        Chrome on macOS

    This is primarily for the user's "Active Sessions" UI.
    """

    user_agent: str | None = Field(
        default=None,
        max_length=1000,
    )
    """
    HTTP User-Agent observed when the session was created.

    Useful for:

    - security auditing
    - session management UI
    - suspicious-login investigation

    User-Agent strings should not be treated as trusted identity.
    """

    ip_address: str | None = Field(
        default=None,
        max_length=45,
    )
    """
    IP address observed when the session was created.

    Supports both IPv4 and IPv6.

    Example:

        192.168.1.10
        2001:db8::1

    This information is useful for security auditing but should
    not be treated as permanent proof of user identity.
    """

    last_ip_address: str | None = Field(
        default=None,
        max_length=45,
    )
    """
    Most recent IP address associated with the session.

    Keeping the initial and latest IP separately makes it possible
    to identify significant changes without overwriting the
    original login information.
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
    UTC timestamp when the session was created.
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    UTC timestamp when the session record was last modified.
    """

    # ============================================================
    # RELATIONSHIP
    # ============================================================

    user: "User" = Relationship(
        back_populates="sessions",
    )
    """
    User owning this authentication session.
    """

