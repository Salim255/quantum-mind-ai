
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlmodel import Field, Relationship, SQLModel


class LearningLevel(str, Enum):
    """
    Supported learner proficiency levels.
    """

    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Profile(SQLModel, table=True):
    """
    User-facing profile.

    Contains personal information and learning preferences.

    Authentication and security information intentionally
    remain outside this entity.
    """

    __tablename__ = "profiles"

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )
    """
    Unique identifier of the profile.
    """

    user_id: UUID = Field(
        nullable=False,
        unique=True,
        foreign_key="users.id",
        index=True,
    )
    """
    User owning this profile.

    UNIQUE guarantees a one-to-one relationship.
    """

    # ============================================================
    # PERSONAL INFORMATION
    # ============================================================

    first_name: str = Field(
        nullable=False,
        max_length=100,
    )
    """
    User's first name.
    """

    last_name: str = Field(
        nullable=False,
        max_length=100,
    )
    """
    User's last name.
    """

    display_name: str | None = Field(
        default=None,
        max_length=100,
    )
    """
    Optional name displayed throughout the application.

    If NULL, the application can derive it from the
    first and last names.
    """

    avatar_url: str | None = Field(
        default=None,
        max_length=1000,
    )
    """
    Reference to the user's avatar stored externally.

    The actual image should not be stored in PostgreSQL.
    """

    bio: str | None = Field(
        default=None,
        max_length=500,
    )
    """
    Optional short user biography.
    """

    # ============================================================
    # LEARNING
    # ============================================================

    learning_level: LearningLevel = Field(
        default=LearningLevel.BEGINNER,
        nullable=False,
        index=True,
    )
    """
    Current learner proficiency level.

    Used for personalization, recommendations,
    difficulty selection and learning paths.
    """

    # ============================================================
    # PREFERENCES
    # ============================================================

    preferred_language: str = Field(
        default="en",
        nullable=False,
        max_length=10,
    )
    """
    Preferred application/content language.

    Examples:
        en
        fr
        ar
    """

    timezone: str = Field(
        default="UTC",
        nullable=False,
        max_length=64,
    )
    """
    IANA timezone used for user-facing dates,
    reminders and scheduled learning activities.

    Example:
        Europe/Paris
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
    Timestamp when the profile was created.
    """

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            DateTime(timezone=True),
            nullable=False,
        ),
    )
    """
    Timestamp of the last profile modification.
    """

    # ============================================================
    # RELATIONSHIP
    # ============================================================

    user: User = Relationship(
        back_populates="profile",
    )
    """
    User owning this profile.
    """

