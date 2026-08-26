from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginDTO(BaseModel):
    """
    Data required to authenticate an existing user.

    Only authentication credentials are accepted.

    Account security state, password hashes, session identifiers,
    and token information are handled internally by the
    authentication service.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    # ============================================================
    # CREDENTIALS
    # ============================================================

    email: EmailStr = Field(
        max_length=255,
        description="Email address associated with the account.",
        examples=["salim@example.com"],
    )

    password: str = Field(
        min_length=1,
        max_length=128,
        description="Account password.",
    )


class RegisterDTO(BaseModel):
    """
    Data required to create a new user account.

    Only client-provided registration data is accepted.
    Account state and security-related fields are controlled
    by the application.
    """

    model_config = ConfigDict(
        str_strip_whitespace=True,
    )

    # ============================================================
    # IDENTITY
    # ============================================================

    email: EmailStr = Field(
        description="User email address.",
    )

    # ============================================================
    # CREDENTIALS
    # ============================================================

    password: str = Field(
        min_length=8,
        description="Plain-text password received during registration.",
    )

    # ============================================================
    # PROFILE
    # ============================================================

    first_name: str = Field(
        min_length=1,
        max_length=100,
        description="User first name.",
    )

    last_name: str = Field(
        min_length=1,
        max_length=100,
        description="User last name.",
    )