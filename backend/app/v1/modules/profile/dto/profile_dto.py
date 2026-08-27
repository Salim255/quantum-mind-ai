from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class ProfileDTO(BaseModel):
    """
    Represents the profile data used by the profile service.

    ProfileDTO contains the user identity and non-authentication
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