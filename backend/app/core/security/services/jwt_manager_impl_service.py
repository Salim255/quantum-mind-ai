import jwt
from uuid import UUID
from datetime import UTC, datetime, timedelta
from app.core.settings import SettingsService
from app.core.security.services.jwt_manager_service import JWTManagerService


class JWTManagerImplService(JWTManagerService):
    """
    JWT implementation based on PyJWT.

    This class contains all JWT-library-specific logic.

    The rest of the application should depend on
    JWTManagerService instead of importing PyJWT directly.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        settings: SettingsService,
    ) -> None:
        """
        Initializes the JWT manager from application settings.
        """

        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM

        self.access_expire_in = (
            settings.JWT_ACCESS_EXPIRE_IN
        )

        self.refresh_expire_in = (
            settings.JWT_REFRESH_EXPIRE_IN
        )

    # ============================================================
    # ACCESS TOKEN
    # ============================================================

    def create_access_token(
        self,
        user_id: UUID,
        session_id: UUID,
    ) -> tuple[str, datetime]:
        """
        Creates a short-lived access token.

        Claims:

        sub:
            User identifier.

        sid:
            Authentication session identifier.

        type:
            Token type.

        iat:
            Time at which the token was issued.

        exp:
            Time at which the token expires.
        """

        return self._create_token(
            user_id=user_id,
            session_id=session_id,
            token_type="access",
            expires_in=self.access_expire_in,
        )

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    def create_refresh_token(
        self,
        user_id: UUID,
        session_id: UUID,
    ) -> tuple[str, datetime]:
        """
        Creates a long-lived refresh token.

        The refresh token is linked to the authenticated session
        through the `sid` claim.
        """

        return self._create_token(
            user_id=user_id,
            session_id=session_id,
            token_type="refresh",
            expires_in=self.refresh_expire_in,
        )

    # ============================================================
    # TOKEN CREATION
    # ============================================================

    def _create_token(
        self,
        user_id: UUID,
        session_id: UUID,
        token_type: str,
        expires_in: int,
    ) -> tuple[str, datetime]:
        """
        Creates and signs a JWT.

        The payload contains only authentication-related claims.

        No sensitive user information should be stored inside
        the JWT because JWT payloads are encoded, not encrypted.
        """

        now = datetime.now(UTC)

        expires_at = now + timedelta(
            minutes=expires_in,
        )

        payload = {
            "sub": str(user_id),
            "sid": str(session_id),
            "type": token_type,
            "iat": now,
            "exp": expires_at,
        }

        token =  jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

        return token, expires_at
    
    # ============================================================
    # TOKEN DECODING
    # ============================================================

    def decode_token(
        self,
        token: str,
    ) -> dict:
        """
        Decodes and validates a JWT.

        PyJWT validates:

        - JWT signature
        - expiration (`exp`)
        - token structure

        An InvalidTokenError is raised when the token cannot
        be trusted.
        """

        return jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
        )