from abc import ABC, abstractmethod
from uuid import UUID


class JWTManagerService(ABC):
    """
    Defines authentication-token operations.

    This service owns JWT/token mechanics.

    It is intentionally independent from FastAPI and database
    persistence.

    Responsibilities:

    - create access tokens
    - decode access tokens
    - validate token claims
    - generate cryptographically secure refresh-token values

    Refresh-token persistence remains the responsibility of
    RefreshTokenRepository.
    """

    # ============================================================
    # ACCESS TOKEN
    # ============================================================

    @abstractmethod
    def create_access_token(
        self,
        user_id: UUID,
        security_version: int,
    ) -> str:
        """
        Creates a short-lived access token.

        The token should contain only the claims required by the API.

        Typical claims:

        - sub: user identifier
        - type: access
        - iat: issued-at timestamp
        - exp: expiration timestamp
        - jti: unique token identifier
        - sv: security version
        """

        raise NotImplementedError

    # ============================================================
    # ACCESS TOKEN VALIDATION
    # ============================================================

    @abstractmethod
    def decode_access_token(
        self,
        token: str,
    ) -> dict:
        """
        Decodes and validates an access token.

        Invalid, expired, malformed, or incorrectly typed tokens
        must be rejected.
        """

        raise NotImplementedError

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    @abstractmethod
    def generate_refresh_token(self) -> str:
        """
        Generates a cryptographically secure refresh-token value.

        The plaintext token is sent to the client through a secure
        HttpOnly cookie.

        Only a hash of the token should be persisted.
        """

        raise NotImplementedError

    # ============================================================
    # TOKEN HASHING
    # ============================================================

    @abstractmethod
    def hash_refresh_token(
        self,
        token: str,
    ) -> str:
        """
        Produces the persistent hash of a refresh token.

        The raw refresh token must never be stored in the database.
        """

        raise NotImplementedError

