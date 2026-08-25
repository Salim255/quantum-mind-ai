from pydantic import BaseModel, Field, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


from pydantic import BaseModel, ConfigDict, EmailStr, Field


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