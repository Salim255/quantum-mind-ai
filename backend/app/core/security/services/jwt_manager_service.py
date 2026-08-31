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