from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserDTO(BaseModel):
    """
    Represents the application-level representation of a user account.

    UserDTO contains the non-sensitive information required to
    represent a persisted user account throughout the application.

    The DTO intentionally excludes authentication credentials and
    security-sensitive information.

    Authentication and security data such as:

    - password
    - password_hash
    - access tokens
    - refresh tokens
    - session identifiers
    - authentication security state
    - failed login counters
    - account lock information

    must never be exposed through this DTO.

    The DTO reflects the state of an existing user account.
    Therefore, fields that are always present on the User entity
    remain required.

    The only optional field is deleted_at because an account is
    not necessarily soft-deleted.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        description="Unique identifier of the user account.",
    )

    email: EmailStr = Field(
        description="Email address associated with the user account.",
    )

    # ============================================================
    # ACCOUNT STATUS
    # ============================================================

    is_active: bool = Field(
        description="Indicates whether the user account is currently active.",
    )

    deleted_at: datetime | None = Field(
        default=None,
        description="UTC timestamp when the account was soft-deleted, if applicable.",
    )

    # ============================================================
    # AUDIT / LIFECYCLE
    # ============================================================

    created_at: datetime = Field(
        description="UTC timestamp when the user account was created.",
    )

    updated_at: datetime = Field(
        description="UTC timestamp when the user account was last modified.",
    )