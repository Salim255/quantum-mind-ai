from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


class LearningLevel(str, Enum):
    """
    Defines the learner's current level.

    Using an enum prevents inconsistent values such as:
    "beginner", "Beginner", "basic", etc.
    """

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class User(SQLModel, table=True):
    """
    Represents a platform user.

    This table contains stable user identity, authentication state,
    account security state, learning profile, and account lifecycle data.

    Temporary security credentials such as refresh tokens, password
    reset tokens, and email verification tokens belong in dedicated
    tables rather than being stored directly on the user.
    """

    __tablename__ = "users"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )
    """
    Unique identifier of the user.

    UUIDs avoid exposing sequential database IDs and provide a stable
    identifier for relationships with other entities such as attempts,
    sessions, progress records, and learning activity.

    Primary key:
        Uniquely identifies each user.

    Index:
        Makes lookups by user ID efficient.
    """

    username: str = Field(
        nullable=False,
        unique=True,
        index=True,
        max_length=50,
    )
    """
    Unique public identity used to identify the learner inside the
    application.

    The unique constraint guarantees that two users cannot have the
    same username.

    The index makes username-based lookups efficient, for example
    during authentication or profile searches.
    """

    avatar_url: str | None = Field(
        default=None,
        max_length=1000,
    )
    """
    URL or storage reference of the user's avatar.

    The actual image is stored outside the database, typically in
    object storage such as S3. This field stores only its reference.

    NULL means that no custom avatar has been configured, allowing
    the frontend to fall back to initials or a default avatar.
    """
    
    email: str = Field(
        nullable=False,
        unique=True,
        index=True,
        max_length=255,
    )
    """
    User's unique email address.

    Used for:
    - authentication
    - account verification
    - password recovery
    - security notifications

    The unique constraint prevents multiple accounts from using
    the same email address.
    """

    # ============================================================
    # AUTHENTICATION
    # ============================================================

    password_hash: str = Field(
        nullable=False,
        max_length=255,
    )
    """
    Secure hash of the user's password.

    The plaintext password must NEVER be stored.

    The application hashes the password before persistence and
    verifies login attempts against this hash.

    A length of 255 leaves enough room for modern password-hashing
    formats such as Argon2 or bcrypt.
    """

    email_verified: bool = Field(
        default=False,
        nullable=False,
        index=True,
    )
    """
    Indicates whether the user has successfully verified ownership
    of their email address.

    Used to restrict sensitive actions until verification is complete
    and to distinguish verified accounts from newly registered ones.

    The index is useful when querying unverified accounts, for example
    during verification or account-maintenance jobs.
    """

    # ============================================================
    # ACCOUNT SECURITY
    # ============================================================

    failed_login_attempts: int = Field(
        default=0,
        nullable=False,
    )
    """
    Number of consecutive failed authentication attempts.

    Used as part of brute-force protection.

    After a configurable number of failures, the account can be
    temporarily locked through `locked_until`.

    This counter should normally be reset after a successful login.
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

    NULL means that the account is not currently locked.

    This allows the application to implement temporary account
    lockout without permanently disabling the user.

    The timezone-aware timestamp is important because the application
    may run across different servers or regions.
    """

    last_login_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp of the user's most recent successful login.

    Useful for:
    - security monitoring
    - account activity
    - detecting unusual inactivity
    - displaying account information

    It should represent a successful authentication, not merely
    an attempted login.
    """

    password_changed_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp of the last password change.

    Useful for security policies such as:
    - invalidating old sessions
    - detecting password changes
    - enforcing password rotation policies when required

    NULL can represent an account that has never changed its password.
    """

    security_version: int = Field(
        default=0,
        nullable=False,
    )
    """
    Global security version for the user's authentication state.

    Incrementing this value can invalidate previously issued
    authentication sessions or tokens.

    Example:
        Password compromised
            ↓
        Increment security_version
            ↓
        Existing sessions become invalid

    This provides a simple mechanism for global session invalidation
    without individually processing every active session.
    """

    # ============================================================
    # ACCOUNT STATUS
    # ============================================================

    is_active: bool = Field(
        default=True,
        nullable=False,
        index=True,
    )
    """
    Indicates whether the account is currently active.

    An inactive user remains in the database but cannot normally
    authenticate or use protected parts of the platform.

    Keeping the account instead of deleting it preserves relationships
    and historical learning data such as quiz attempts.
    """

    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    Timestamp indicating that the account has been soft-deleted.

    NULL means the account has not been deleted.

    Soft deletion is useful because learning records such as attempts,
    scores, and activity may need to remain for data integrity,
    auditing, or business requirements.

    The actual account visibility/access rules should use this field
    together with `is_active`.
    """

    # ============================================================
    # LEARNING PROFILE
    # ============================================================

    level: LearningLevel = Field(
        default=LearningLevel.BEGINNER,
        nullable=False,
        index=True,
    )
    """
    Current learning level of the user.

    Used to personalize the learning experience, for example:
    - recommending appropriate topics
    - selecting quiz difficulty
    - adapting learning paths
    - displaying learner progress

    The enum guarantees that only supported learning levels can
    be stored.

    The index allows efficient filtering of learners by level.
    """

    # ============================================================
    # AUDIT / LIFECYCLE
    # ============================================================

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    Timestamp when the user account was created.

    Used for:
    - account history
    - analytics
    - auditing
    - retention calculations

    UTC is used as the canonical storage timezone so timestamps
    remain consistent across environments.
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    Timestamp of the last modification to the user record.

    Should be updated whenever mutable user information changes.

    Keeping this timestamp allows the application to know when the
    record was last modified without inspecting individual fields.

    The database stores the timestamp with timezone information and
    the application uses UTC as the canonical timezone.
    """