from typing import Annotated

from fastapi import Depends, status

from app.core.dtos.response_dto import ResponseDTO

from app.v1.modules.auth.dependencies import dependencies
from app.v1.modules.auth.dto.auth_dto import (LoginDTO, RegisterDTO, AuthResponseDTO)

from app.v1.modules.auth.service.auth_service import AuthService

from .router import router as auth_router


# ==========================================================
# REGISTER
# ==========================================================

@auth_router.post(
    "/register",
    response_model=ResponseDTO[AuthResponseDTO],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="""
Creates a new QuantumMind user account.

The registration process is handled by the authentication service.

The service is responsible for:

- validating the registration data
- checking email uniqueness
- hashing the password
- creating the user
- creating the user profile
- creating the user security record
- creating the initial session
- issuing authentication tokens
""",
    responses={
        201: {
            "description": "User successfully registered."
        },
        400: {
            "description": "Invalid registration data."
        },
        409: {
            "description": "An account with the provided email already exists."
        },
    },
)
async def register(
    payload: AuthRegisterDTO,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> ResponseDTO[AuthResponseDTO]:

    return ResponseDTO.success(
        await auth_service.register(payload)
    )


# ==========================================================
# LOGIN
# ==========================================================

@auth_router.post(
    "/login",
    response_model=ResponseDTO[AuthResponseDTO],
    status_code=status.HTTP_200_OK,
    summary="Authenticate a user",
    description="""
Authenticates an existing QuantumMind user.

The authentication service validates the credentials,
checks the account security state, creates an authenticated
session, and issues the required authentication tokens.
""",
    responses={
        200: {
            "description": "User successfully authenticated."
        },
        401: {
            "description": "Invalid authentication credentials."
        },
        403: {
            "description": "User account is inactive or locked."
        },
    },
)
async def login(
    payload: AuthLoginDTO,
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
) -> ResponseDTO[AuthResponseDTO]:

    return ResponseDTO.success(
        await auth_service.login(payload)
    )