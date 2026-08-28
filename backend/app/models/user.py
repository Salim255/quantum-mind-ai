from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """
    Represents the core platform account.

    This table is intentionally kept small.

    User is responsible only for stable account identity,
    authentication credentials, account lifecycle, and
    relationships to the user's profile and security state.

    Personal information belongs to Profile.

    Authentication security state belongs to UserSecurity.

    Refresh-token/session state belongs to UserSession.

    Learning activity belongs to the corresponding learning
    domain tables.

    This separation keeps the account model maintainable,
    secure, and easy to evolve as the application grows.
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
    Stable unique identifier of the account.

    UUIDs prevent exposing predictable sequential identifiers
    and provide a stable reference for relationships throughout
    the application.

    Examples of entities referencing this ID:

    - Profile
    - UserSecurity
    - UserSession
    - QuizAttempt
    - UserQuestionProgress
    """

    email: str = Field(
        nullable=False,
        unique=True,
        index=True,
        max_length=255,
    )
    """
    Unique email address associated with the account.

    Used as the primary login identifier and for account-related
    communication such as:

    - email verification
    - password reset
    - security notifications
    - account recovery

    The database UNIQUE constraint guarantees that an email
    address belongs to at most one account.

    Email verification state itself belongs to UserSecurity.
    """

    # ============================================================
    # AUTHENTICATION CREDENTIAL
    # ============================================================

    password_hash: str = Field(
        nullable=False,
        max_length=255,
    )
    """
    Secure password hash.

    The application must NEVER store the user's plaintext password.

    Passwords should be hashed using a modern password hashing
    algorithm such as Argon2id before being persisted.

    The authentication service is responsible for:

        plaintext password
                ↓
            password hash
                ↓
            database

    Password-change metadata belongs to UserSecurity.
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

    False means the account is administratively disabled and
    should normally not be allowed to authenticate.

    This is intentionally different from a temporary security
    lockout.

    Example:

        is_active = False
            → administrator disabled the account

        locked_until = future timestamp
            → temporary authentication protection
    """

    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            DateTime(timezone=True),
            nullable=True,
        ),
    )
    """
    UTC timestamp when the account was soft-deleted.

    NULL means the account has not been deleted.

    Soft deletion allows historical domain data such as:

    - attempts
    - progress
    - scores
    - learning activity

    to remain associated with the account.

    Application queries should normally exclude users where
    deleted_at IS NOT NULL.

    If the application does not require soft deletion, this
    field can be removed entirely.
    """

    # ============================================================
    # RELATIONSHIPS
    # ============================================================

    profile: "Profile" = Relationship(
        back_populates="user"
    )
    """
    One-to-one relationship with the user's Profile.

    Profile contains information such as:

    - first name
    - last name
    - display name
    - avatar
    - biography
    - learning level
    - language
    - timezone

    Keeping these fields outside User prevents the authentication
    model from becoming a large user-profile aggregate.
    """

    security: "UserSecurity" = Relationship(
        back_populates="user"
    )
    """
    One-to-one relationship with UserSecurity.

    UserSecurity contains security state such as:

    - email verification
    - failed login attempts
    - temporary lockout
    - last login
    - password change timestamp
    - security version
    - MFA state

    Security state is separated because it changes independently
    from the user's core identity.
    """

    sessions: list["UserSession"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
    """
    One-to-many relationship with authentication sessions.

    A single account can have multiple active sessions:

        User
          ├── Mac session
          ├── Mobile session
          └── Browser session

    Refresh tokens should be represented by UserSession records
    rather than being stored directly on the User table.
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
    UTC timestamp when the account was created.

    Useful for:

    - auditing
    - analytics
    - account lifecycle management
    - retention analysis
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    UTC timestamp of the last modification to the account.

    This should be updated whenever mutable User fields change.

    Security-specific modifications should update UserSecurity's
    own updated_at timestamp instead.
    """
