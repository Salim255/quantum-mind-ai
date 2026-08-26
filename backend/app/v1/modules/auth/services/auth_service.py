from abc import ABC, abstractmethod

from app.v1.modules.auth.dto.auth_dto import (LoginDTO, RegisterDTO, AuthResponseDTO)


class AuthService(ABC):
    """
    Defines the application-level authentication contract.

    AuthService is responsible for exposing authentication use cases
    without coupling controllers to their implementation.

    The implementation coordinates:

    - UserRepository
    - ProfileRepository
    - UserSecurityRepository
    - UserSessionRepository
    - RefreshTokenRepository
    - password hashing
    - token generation
    - authentication security rules

    Controllers should depend on this abstraction rather than on
    AuthImplService directly.
    """

    # ============================================================
    # REGISTER
    # ============================================================

    @abstractmethod
    async def register(
        self,
        payload: RegisterDTO,
    ) -> AuthResponseDTO:
        """
        Creates a new user account.

        The registration workflow is responsible for creating the
        account and its associated authentication state.

        Expected workflow:

            User
              +
            Profile
              +
            UserSecurity
              +
            UserSession
              +
            RefreshToken

        The complete operation should be transactional so that
        an account is not partially created.

        Authentication credentials are delivered through secure
        HttpOnly cookies rather than through the response body.
        """

        raise NotImplementedError

    # ============================================================
    # LOGIN
    # ============================================================

    @abstractmethod
    async def login(
        self,
        payload: LoginDTO,
    ) -> AuthResponseDTO:
        """
        Authenticates an existing user.

        The implementation is responsible for:

        - locating the user
        - validating the password
        - checking account status
        - checking authentication security state
        - handling failed login attempts
        - creating an authenticated session
        - creating or rotating the refresh token
        - issuing authentication cookies
        - updating login metadata

        Access and refresh tokens are never returned through the
        AuthResponseDTO. They are delivered using secure HttpOnly
        cookies.
        """

        raise NotImplementedError

