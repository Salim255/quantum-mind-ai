from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserSessionDTO(BaseModel):
    """
    Represents an authenticated user session.

    UserSessionDTO contains the session identity, refresh-token
    state, lifecycle information, security version and client
    metadata required to work with an authenticated session.

    This DTO can be used across session creation, retrieval,
    refresh-token rotation, revocation and session management
    workflows.

    The raw refresh token must never be stored or exposed through
    this DTO. Only the cryptographic hash persisted by the session
    service is represented here.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    id: UUID = Field(
        description="Unique identifier of the authenticated session.",
    )

    user_id: UUID = Field(
        description="Unique identifier of the user owning the session.",
    )

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    refresh_token_hash: str = Field(
        description="Cryptographic hash of the current refresh token.",
    )

    token_version: int = Field(
        description="Current refresh-token version for the session.",
    )

    previous_token_hash: str | None = Field(
        default=None,
        description=(
            "Cryptographic hash of the immediately previous "
            "refresh token used for rotation and replay detection."
        ),
    )

    # ============================================================
    # SESSION LIFECYCLE
    # ============================================================

    expires_at: datetime = Field(
        description="UTC timestamp when the session expires.",
    )

    last_used_at: datetime | None = Field(
        default=None,
        description="UTC timestamp when the session was last successfully used.",
    )

    revoked_at: datetime | None = Field(
        default=None,
        description="UTC timestamp when the session was revoked.",
    )

    # ============================================================
    # SECURITY VERSION
    # ============================================================

    security_version: int = Field(
        description=(
            "Security version captured when the session was created."
        ),
    )

    # ============================================================
    # DEVICE / CLIENT INFORMATION
    # ============================================================

    device_name: str | None = Field(
        default=None,
        description="Human-readable name identifying the client device or session.",
    )

    user_agent: str | None = Field(
        default=None,
        description="HTTP User-Agent observed when the session was created.",
    )

    ip_address: str | None = Field(
        default=None,
        description="IP address observed when the session was created.",
    )

    last_ip_address: str | None = Field(
        default=None,
        description="Most recent IP address associated with the session.",
    )

    # ============================================================
    # AUDIT
    # ============================================================

    created_at: datetime = Field(
        description="UTC timestamp when the session was created.",
    )

    updated_at: datetime = Field(
        description="UTC timestamp when the session was last modified.",
    )