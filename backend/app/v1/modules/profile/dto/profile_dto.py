from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime

from app.models.profile import LearningLevel


class CreateProfileDTO(BaseModel):
    """
    Represents the profile data used by the profile service.

    CreateProfileDTO contains the user identity and non-authentication
    information required to create or represent a user profile.

    The user identifier is included in this DTO because it defines
    which user the profile belongs to.

    This DTO must only contain profile-related information and must
    never contain authentication or security-related data such as:

    - password
    - password_hash
    - access tokens
    - refresh tokens
    - session identifiers
    - security information
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # USER
    # ============================================================

    user_id: UUID = Field(
        description="Unique identifier of the user associated with the profile.",
    )

    # ============================================================
    # PROFILE
    # ============================================================

    first_name: str = Field(
        description="First name associated with the user profile.",
    )

    last_name: str = Field(
        description="Last name associated with the user profile.",
    )


class ProfileDTO(BaseModel):
    """
    Represents a complete user profile.

    ProfileDTO is used to transfer profile data between the
    application layers after a profile has been created or retrieved.

    It contains only user-facing profile information and profile
    metadata.

    Authentication and security information intentionally remain
    outside this DTO.

    Sensitive authentication data such as:

    - password
    - password_hash
    - access tokens
    - refresh tokens
    - session identifiers
    - security information

    must never be exposed through this DTO.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        description="Unique identifier of the profile.",
    )

    user_id: UUID = Field(
        description="Unique identifier of the user who owns the profile.",
    )

    # ============================================================
    # PERSONAL INFORMATION
    # ============================================================

    first_name: str = Field(
        description="First name stored in the profile.",
    )

    last_name: str = Field(
        description="Last name stored in the profile.",
    )

    display_name: str | None = Field(
        description="Optional name displayed throughout the application.",
    )

    avatar_url: str | None = Field(
        description="Optional reference to the user's externally stored avatar.",
    )

    bio: str | None = Field(
        description="Optional short biography associated with the profile.",
    )

    # ============================================================
    # LEARNING
    # ============================================================

    learning_level: LearningLevel = Field(
        description="Current learner proficiency level.",
    )

    # ============================================================
    # PREFERENCES
    # ============================================================

    preferred_language: str = Field(
        description="Preferred application and content language.",
    )

    timezone: str = Field(
        description="IANA timezone used for user-facing dates and scheduled activities.",
    )

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime = Field(
        description="Timestamp when the profile was created.",
    )

    updated_at: datetime = Field(
        description="Timestamp when the profile was last modified.",
    )