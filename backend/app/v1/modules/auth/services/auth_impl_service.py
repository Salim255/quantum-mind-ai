from datetime import UTC, datetime, timedelta

from app.repositories.profile_repository import ProfileRepository
from app.repositories.user_repository import UserRepository
from app.repositories.user_security_repository import UserSecurityRepository
from app.repositories.user_session_repository import UserSessionRepository

from app.v1.modules.auth.dto.auth_dto import (LoginDTO, RegisterDTO, AuthResponseDTO)
from app.v1.modules.auth.services.auth_service import AuthService
from app.common.constants import (ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS)

class AuthImplService(AuthService):
    """
    Concrete implementation of the authentication service.

    AuthImplService orchestrates the complete authentication workflow.

    Responsibilities:

    - register new accounts
    - authenticate existing accounts
    - coordinate User and related authentication tables
    - enforce authentication security rules
    - create authenticated sessions
    - generate access and refresh credentials
    - return a safe authentication response

    Database access remains inside repositories.

    HTTP concerns such as setting cookies remain inside the controller.
    """
 
    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        user_repository: UserRepository,
        user_security_repository: UserSecurityRepository,
        user_session_repository: UserSessionRepository,
        profile_repository: ProfileRepository,
    ) -> None:
        """
        Initializes the authentication service.

        Repositories are injected through the dependency layer,
        keeping the service independent from FastAPI's dependency
        injection mechanism.
        """

        self.user_repository = user_repository
        self.user_security_repository = user_security_repository
        self.user_session_repository = user_session_repository
        self.profile_repository = profile_repository

    # ============================================================
    # REGISTER
    # ============================================================

    async def register(
        self,
        payload: RegisterDTO,
    ) -> AuthResponseDTO:
        """
        Registers a new user account.

        Registration performs the following high-level workflow:

            1. Validate account uniqueness
            2. Hash the password
            3. Create User
            4. Create Profile
            5. Create UserSecurity
            6. Create authenticated session
            7. Create refresh-token state
            8. Generate authentication credentials
            9. Return safe user information

        The plaintext password is never persisted.

        Authentication credentials are not returned through the
        public AuthResponseDTO.
        """

        # --------------------------------------------------------
        # CHECK ACCOUNT UNIQUENESS
        # --------------------------------------------------------

        existing_user = await self.user_repository.get_by_email(
            payload.email
        )

        if existing_user is not None:
            raise ValueError(
                "An account with this email already exists."
            )

        # --------------------------------------------------------
        # PASSWORD HASHING
        # --------------------------------------------------------

        password_hash = self._hash_password(
            payload.password
        )

        # --------------------------------------------------------
        # CREATE USER
        # --------------------------------------------------------

        user = await self.user_repository.create(
            {
                "email": payload.email,
                "password_hash": password_hash,
                "email_verified": False,
                "is_active": True,
            }
        )

        # --------------------------------------------------------
        # CREATE PROFILE
        # --------------------------------------------------------

        await self.profile_repository.create(
            {
                "user_id": user.id,
                "first_name": payload.first_name,
                "last_name": payload.last_name,
            }
        )

        # --------------------------------------------------------
        # CREATE SECURITY STATE
        # --------------------------------------------------------

        await self.user_security_repository.create(
            {
                "user_id": user.id,
            }
        )

        # --------------------------------------------------------
        # CREATE AUTHENTICATED SESSION
        # --------------------------------------------------------

        session = await self.user_session_repository.create(
            {
                "user_id": user.id,
                "created_at": datetime.now(UTC),
            }
        )

        # --------------------------------------------------------
        # CREATE REFRESH TOKEN
        # --------------------------------------------------------

        refresh_token = self._generate_refresh_token()

        refresh_token_hash = self._hash_token(
            refresh_token
        )

        refresh_expires_at = (
            datetime.now(UTC)
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        await self.refresh_token_repository.create(
            {
                "session_id": session.id,
                "token_hash": refresh_token_hash,
                "expires_at": refresh_expires_at,
            }
        )

        # --------------------------------------------------------
        # GENERATE ACCESS TOKEN
        # --------------------------------------------------------

        access_token = self._generate_access_token(
            user_id=user.id,
        )

        # --------------------------------------------------------
        # RETURN SAFE RESPONSE
        # --------------------------------------------------------

        return AuthResponseDTO(
            user_id=user.id,
            email=user.email,
        )

    # ============================================================
    # LOGIN
    # ============================================================

    async def login(
        self,
        payload: LoginDTO,
    ) -> AuthResponseDTO:
        """
        Authenticates an existing user.

        Login performs:

            1. Locate account
            2. Check account status
            3. Check temporary lock
            4. Verify password
            5. Handle failed authentication
            6. Reset security counters
            7. Create session
            8. Create refresh-token state
            9. Generate access credential
            10. Return safe user information
        """

        # --------------------------------------------------------
        # FIND USER
        # --------------------------------------------------------

        user = await self.user_repository.get_by_email(
            payload.email
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        # --------------------------------------------------------
        # CHECK ACCOUNT STATUS
        # --------------------------------------------------------

        if not user.is_active:
            raise ValueError(
                "This account is inactive."
            )

        if user.deleted_at is not None:
            raise ValueError(
                "This account is no longer available."
            )

        # --------------------------------------------------------
        # LOAD SECURITY STATE
        # --------------------------------------------------------

        security = (
            await self.user_security_repository.get_by_user_id(
                user.id
            )
        )

        if security is None:
            raise ValueError(
                "Authentication security state is unavailable."
            )

        # --------------------------------------------------------
        # CHECK ACCOUNT LOCK
        # --------------------------------------------------------

        now = datetime.now(UTC)

        if (
            security.locked_until is not None
            and security.locked_until > now
        ):
            raise ValueError(
                "Too many failed login attempts. "
                "Please try again later."
            )

        # --------------------------------------------------------
        # VERIFY PASSWORD
        # --------------------------------------------------------

        password_valid = self._verify_password(
            payload.password,
            user.password_hash,
        )

        if not password_valid:

            await self._handle_failed_login(
                user.id,
                security,
            )

            # Never reveal whether the email exists or the password
            # was the incorrect credential.
            raise ValueError(
                "Invalid email or password."
            )

        # --------------------------------------------------------
        # RESET LOGIN SECURITY STATE
        # --------------------------------------------------------

        await self.user_security_repository.update(
            security.id,
            {
                "failed_login_attempts": 0,
                "locked_until": None,
            },
        )

        # --------------------------------------------------------
        # UPDATE LOGIN INFORMATION
        # --------------------------------------------------------

        await self.user_repository.update(
            user.id,
            {
                "last_login_at": now,
            },
        )

        # --------------------------------------------------------
        # CREATE SESSION
        # --------------------------------------------------------

        session = await self.user_session_repository.create(
            {
                "user_id": user.id,
                "created_at": now,
            }
        )

        # --------------------------------------------------------
        # CREATE REFRESH TOKEN
        # --------------------------------------------------------

        refresh_token = self._generate_refresh_token()

        refresh_token_hash = self._hash_token(
            refresh_token
        )

        refresh_expires_at = (
            now
            + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        )

        await self.refresh_token_repository.create(
            {
                "session_id": session.id,
                "token_hash": refresh_token_hash,
                "expires_at": refresh_expires_at,
            }
        )

        # --------------------------------------------------------
        # GENERATE ACCESS TOKEN
        # --------------------------------------------------------

        access_token = self._generate_access_token(
            user_id=user.id,
        )

        # --------------------------------------------------------
        # RETURN SAFE RESPONSE
        # --------------------------------------------------------

        return AuthResponseDTO(
            user_id=user.id,
            email=user.email,
        )

    # ============================================================
    # FAILED LOGIN
    # ============================================================

    async def _handle_failed_login(
        self,
        user_id,
        security,
    ) -> None:
        """
        Handles a failed authentication attempt.

        The counter is incremented and the account is temporarily
        locked after the configured threshold.

        The exact threshold and lock duration should eventually be
        moved into application configuration.
        """

        failed_attempts = (
            security.failed_login_attempts + 1
        )

        update_data = {
            "failed_login_attempts": failed_attempts,
        }

        if failed_attempts >= 5:
            update_data["locked_until"] = (
                datetime.now(UTC)
                + timedelta(minutes=15)
            )

        await self.user_security_repository.update(
            security.id,
            update_data,
        )

    # ============================================================
    # PASSWORD HASHING
    # ============================================================

    def _hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hashes a plaintext password.

        Replace this implementation with the application's
        configured password-hashing service.

        Argon2id should be preferred for password hashing.
        """

        raise NotImplementedError(
            "Password hashing must be provided by the "
            "application security service."
        )

    # ============================================================
    # PASSWORD VERIFICATION
    # ============================================================

    def _verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verifies a plaintext password against its stored hash.

        The actual hashing implementation should be delegated to
        the application's password security component.
        """

        raise NotImplementedError(
            "Password verification must be provided by the "
            "application security service."
        )

    # ============================================================
    # ACCESS TOKEN
    # ============================================================

    def _generate_access_token(
        self,
        user_id,
    ) -> str:
        """
        Generates a short-lived access token.

        The access token should contain only the minimum claims
        required by the API.

        Typical claims:

        - sub: user identifier
        - iat: issued-at timestamp
        - exp: expiration timestamp
        - jti: unique token identifier
        """

        raise NotImplementedError(
            "Access-token generation must be provided by the "
            "application security service."
        )

    # ============================================================
    # REFRESH TOKEN
    # ============================================================

    def _generate_refresh_token(self) -> str:
        """
        Generates a cryptographically secure refresh token.

        Only its hash should be persisted in the database.
        """

        raise NotImplementedError(
            "Refresh-token generation must be provided by the "
            "application security service."
        )

    # ============================================================
    # TOKEN HASHING
    # ============================================================

    def _hash_token(
        self,
        token: str,
    ) -> str:
        """
        Creates a one-way hash of a refresh token.

        The plaintext refresh token is sent to the client through
        an HttpOnly cookie but is never persisted in plaintext.
        """

        raise NotImplementedError(
            "Token hashing must be provided by the "
            "application security service."
        )

