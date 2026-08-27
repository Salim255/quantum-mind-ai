
from app.v1.modules.auth.dto.auth_dto import (LoginDTO, RegisterDTO, AuthResponseDTO)

from app.v1.modules.auth.services.auth_service import AuthService
from app.v1.modules.auth.services.cookie_service import CookieService
from app.v1.modules.auth.services.jwt_manager_service import (
    JWTManagerService,
)
from app.v1.modules.auth.services.password_service import (
    PasswordService,
)

from app.v1.modules.user.services.user_service import UserService

from app.v1.modules.profile.services.profile_service import (
    ProfileService,
)

from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)

from app.v1.modules.user_session.services.user_session_service import (
    UserSessionService,
)


class AuthImplService(AuthService):
    """
    Concrete implementation of the authentication service.

    AuthImplService is an application-level orchestration service.

    Its responsibility is to coordinate the complete authentication
    workflow without directly managing persistence or infrastructure.

    It coordinates:

    - user account creation and retrieval
    - profile initialization
    - password hashing and verification
    - authentication security state
    - authenticated session lifecycle
    - JWT creation
    - authentication cookies

    Domain-specific operations remain delegated to their respective
    services.

    AuthImplService should not directly access repositories.
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        user_service: UserService,
        profile_service: ProfileService,
        user_security_service: UserSecurityService,
        user_session_service: UserSessionService,
        password_service: PasswordService,
        jwt_manager_service: JWTManagerService,
        cookie_service: CookieService,
    ) -> None:
        """
        Initializes the authentication service.

        Dependencies are injected through abstractions.

        UserService:
            Manages user account operations.

        ProfileService:
            Manages user profile operations.

        UserSecurityService:
            Manages persistent authentication security state.

        UserSessionService:
            Manages authenticated sessions and their lifecycle.

        PasswordService:
            Hashes and verifies passwords.

        JWTManagerService:
            Creates and validates JWT credentials.

        CookieService:
            Writes and clears authentication cookies.
        """

        self.user_service = user_service

        self.profile_service = profile_service

        self.user_security_service = (
            user_security_service
        )

        self.user_session_service = (
            user_session_service
        )

        self.password_service = password_service

        self.jwt_manager_service = jwt_manager_service

        self.cookie_service = cookie_service

    # ============================================================
    # REGISTER
    # ============================================================

    async def register(
        self,
        payload: RegisterDTO,
    ) -> AuthResponseDTO:
        """
        Registers a new platform account.

        Registration workflow:

        1. Check whether the email is already registered.
        2. Hash the plaintext password.
        3. Create the user account.
        4. Create the user's profile.
        5. Initialize the user's security state.
        6. Create an authenticated session.
        7. Generate authentication tokens.

        Domain operations are delegated to their dedicated services.
        """

        # --------------------------------------------------------
        # CHECK EXISTING USER
        # --------------------------------------------------------

        existing_user = await (
            self.user_service.get_user_by_email(
                payload.email
            )
        )

        if existing_user is not None:
            raise ValueError(
                "A user with this email already exists."
            )

        # --------------------------------------------------------
        # HASH PASSWORD
        # --------------------------------------------------------

        password_hash = (
            self.password_service.hash_password(
                payload.password
            )
        )

        # --------------------------------------------------------
        # CREATE USER
        # --------------------------------------------------------

        user = await self.user_service.create_user(
            email=payload.email,
            password_hash=password_hash,
        )

        # --------------------------------------------------------
        # CREATE PROFILE
        # --------------------------------------------------------

        await self.profile_service.create_profile(
            user_id=user.id,
            first_name=payload.first_name,
            last_name=payload.last_name,
        )

        # --------------------------------------------------------
        # INITIALIZE SECURITY STATE
        # --------------------------------------------------------

        await self.user_security_service.create_security(
            user_id=user.id,
        )

        # --------------------------------------------------------
        # CREATE AUTHENTICATED SESSION
        # --------------------------------------------------------

        session = await (
            self.user_session_service.create_session(
                user_id=user.id,
            )
        )

        # --------------------------------------------------------
        # GENERATE ACCESS TOKEN
        # --------------------------------------------------------

        access_token = (
            self.jwt_manager.create_access_token(
                user_id=user.id,
                session_id=session.id,
            )
        )

        # --------------------------------------------------------
        # GENERATE REFRESH TOKEN
        # --------------------------------------------------------

        refresh_token = (
            self.jwt_manager.create_refresh_token(
                user_id=user.id,
                session_id=session.id,
            )
        )

        # --------------------------------------------------------
        # RETURN AUTH RESPONSE
        # --------------------------------------------------------

        return AuthResponseDTO(
            user_id=user.id,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
        )

    # ============================================================
    # LOGIN
    # ============================================================

    async def login(
        self,
        payload: LoginDTO,
    ) -> AuthResponseDTO:
        """
        Authenticates a user.

        Login workflow:

        1. Retrieve the user by email.
        2. Verify that the account is active.
        3. Retrieve the user's security state.
        4. Verify that the account is not locked.
        5. Verify the password.
        6. Register a failed attempt when authentication fails.
        7. Reset security counters when authentication succeeds.
        8. Create a new authenticated session.
        9. Generate authentication tokens.
        """

        # --------------------------------------------------------
        # RETRIEVE USER
        # --------------------------------------------------------

        user = await (
            self.user_service.get_user_by_email(
                payload.email
            )
        )

        # --------------------------------------------------------
        # PREVENT USER ENUMERATION
        # --------------------------------------------------------

        if user is None:

            # Perform a password verification even when the user
            # does not exist to reduce timing differences between
            # valid and invalid accounts.

            self.password_service.verify_password(
                payload.password,
                self.user_security_service.dummy_password_hash,
            )

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

        # --------------------------------------------------------
        # CHECK ACCOUNT DELETION
        # --------------------------------------------------------

        if user.deleted_at is not None:
            raise ValueError(
                "Invalid email or password."
            )

        # --------------------------------------------------------
        # RETRIEVE SECURITY STATE
        # --------------------------------------------------------

        security = await (
            self.user_security_service.get_security_by_user_id(
                user.id
            )
        )

        # --------------------------------------------------------
        # CHECK ACCOUNT LOCK
        # --------------------------------------------------------

        if await (
            self.user_security_service.is_account_locked(
                security
            )
        ):
            raise ValueError(
                "This account is temporarily locked."
            )

        # --------------------------------------------------------
        # VERIFY PASSWORD
        # --------------------------------------------------------

        password_valid = (
            self.password_service.verify_password(
                payload.password,
                user.password_hash,
            )
        )

        if not password_valid:

            await (
                self.user_security_service.handle_failed_login(
                    security
                )
            )

            raise ValueError(
                "Invalid email or password."
            )

        # --------------------------------------------------------
        # SUCCESSFUL AUTHENTICATION
        # --------------------------------------------------------

        await (
            self.user_security_service.handle_successful_login(
                security
            )
        )

        # --------------------------------------------------------
        # CREATE AUTHENTICATED SESSION
        # --------------------------------------------------------

        session = await (
            self.user_session_service.create_session(
                user_id=user.id,
            )
        )

        # --------------------------------------------------------
        # GENERATE ACCESS TOKEN
        # --------------------------------------------------------

        access_token = (
            self.jwt_manager.create_access_token(
                user_id=user.id,
                session_id=session.id,
            )
        )

        # --------------------------------------------------------
        # GENERATE REFRESH TOKEN
        # --------------------------------------------------------

        refresh_token = (
            self.jwt_manager.create_refresh_token(
                user_id=user.id,
                session_id=session.id,
            )
        )

        # --------------------------------------------------------
        # RETURN AUTHENTICATION RESPONSE
        # --------------------------------------------------------

        return AuthResponseDTO(
            user_id=user.id,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
        )