from abc import ABC, abstractmethod
from uuid import UUID


class JWTManagerService(ABC):
    """
    Defines the contract for JWT management.

    This abstraction keeps the authentication layer independent
    from the JWT implementation library.

    The concrete implementation is responsible for:

    - creating access tokens
    - creating refresh tokens
    - decoding and validating tokens
    - validating JWT signatures
    - validating token expiration
    """

    # ============================================================
    # ACCESS TOKEN
    # ============================================================

    @abstractmethod
    def create_access_token(
        self,
        user_id: UUID,
        session_id: UUID,
    ) -> str:
        """
        Creates a short-lived access token.

        The token identifies:

        - the authenticated user
        - the authenticated session

        Returns:
            Encoded and signed JWT.
        """

        raise NotImplementedError

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    @abstractmethod
    def create_refresh_token(
        self,
        user_id: UUID,
        session_id: UUID,
    ) -> str:
        """
        Creates a long-lived refresh token.

        The refresh token is associated with a specific
        authenticated session.

        Returns:
            Encoded and signed JWT.
        """

        raise NotImplementedError

    # ============================================================
    # DECODE TOKEN
    # ============================================================

    @abstractmethod
    def decode_token(
        self,
        token: str,
    ) -> dict:
        """
        Decodes and validates a JWT.

        Validation includes:

        - token signature
        - token expiration
        - JWT structure

        Raises:
            InvalidTokenError:
                When the token cannot be trusted.
        """

        raise NotImplementedError


    # ============================================================
    # VERIFY ACCESS TOKEN
    # ============================================================

    @abstractmethod
    def verify_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Verifies an access token.

        This method is specifically intended for authentication
        middleware and other components that need to establish
        whether an incoming request is authenticated.

        The implementation must verify:

        - JWT signature
        - token expiration
        - token structure
        - token type
        - required access-token claims

        Returns:
            Decoded access-token claims when the token is valid.

        Raises:
            UnauthorizedException:
                When the access token is missing required claims,
                invalid, expired, or otherwise cannot be trusted.
        """

        raise NotImplementedError