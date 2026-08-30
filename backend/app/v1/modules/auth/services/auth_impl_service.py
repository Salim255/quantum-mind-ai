import logging

from app.core.exceptions.auth_exception import (
    AccountInactiveException,
    AccountLockedException,
    EmailAlreadyExistsException,
    InvalidCredentialsException,
)

from app.core.exceptions.base_exception import AppException
from app.core.exceptions.custom_exceptions import ProcessingException
from app.core.exceptions.error_code import ErrorCode

from app.v1.modules.auth.dto.auth_dto import (
    AuthResponseDTO,
    LoginDTO,
    RegisterDTO,
)

from app.v1.modules.auth.services.auth_service import AuthService
from app.v1.modules.auth.services.cookie_service import CookieService

from app.v1.modules.auth.services.jwt_manager_service import (
    JWTManagerService,
)

from app.v1.modules.auth.services.password_service import (
    PasswordService,
)

from app.v1.modules.profile.services.profile_service import (
    ProfileService,
)

from app.v1.modules.user.services.user_service import (
    UserService,
)

from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)

from app.v1.modules.user_session.services.user_session_service import (
    UserSessionService,
)

from app.v1.modules.profile.dto.profile_dto import CreateProfileDTO

logger = logging.getLogger(__name__)


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

        self.jwt_manager_service = (
            jwt_manager_service
        )

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

        Known application exceptions are propagated unchanged.

        Unexpected exceptions are converted into a generic processing
        exception with an authentication-specific error code.
        """

        try:

            # ----------------------------------------------------
            # CHECK EXISTING USER
            # ----------------------------------------------------

            existing_user = await (
                self.user_service.get_user_by_email(
                    payload.email
                )
            )

            if existing_user is not None:
                raise EmailAlreadyExistsException()

            # ----------------------------------------------------
            # HASH PASSWORD
            # ----------------------------------------------------

            password_hash = (
                self.password_service.hash_password(
                    payload.password
                )
            )

            # ----------------------------------------------------
            # CREATE USER
            # ----------------------------------------------------

            user = await self.user_service.create_user(
                email=payload.email,
                password_hash=password_hash,
            )

            # ----------------------------------------------------
            # CREATE PROFILE
            # ----------------------------------------------------
            
            await self.profile_service.create_profile(
                CreateProfileDTO(
                    user_id=user.id,
                    first_name=payload.first_name,
                    last_name=payload.last_name,
                )
            )

            # ----------------------------------------------------
            # INITIALIZE SECURITY STATE
            # ----------------------------------------------------

            security = await (
                self.user_security_service.create_security(
                    user_id=user.id,
                )
            )

            # ----------------------------------------------------
            # CREATE AUTHENTICATED SESSION
            # ----------------------------------------------------

            session = await (
                self.user_session_service.create_session(
                    user_id=user.id,
                    security_version=security.security_version,
                )
            )

            # ----------------------------------------------------
            # GENERATE ACCESS TOKEN
            # ----------------------------------------------------

            access_token = (
                self.jwt_manager_service.create_access_token(
                    user_id=user.id,
                    session_id=session.id,
                )
            )

            # ----------------------------------------------------
            # GENERATE REFRESH TOKEN
            # ----------------------------------------------------

            refresh_token, refresh_token_expires_at = (
                self.jwt_manager_service.create_refresh_token(
                    user_id=user.id,
                    session_id=session.id,
                )
            )

            # ----------------------------------------------------
            # HASH REFRESH TOKEN
            # ----------------------------------------------------

            refresh_token_hash = (
                self.password_service.hash_password(
                    refresh_token
                )
            )

            # ----------------------------------------------------
            # STORE REFRESH TOKEN HASH
            # ----------------------------------------------------

            await self.user_session_service.update_refresh_token(
                session_id=session.id,
                refresh_token_hash=refresh_token_hash,
                expires_at=refresh_token_expires_at
            )

            # ----------------------------------------------------
            # RETURN AUTH RESPONSE
            # ----------------------------------------------------

            return AuthResponseDTO(
                user_id=user.id,
                email=user.email,
                access_token=access_token,
                refresh_token=refresh_token,
            )

        # --------------------------------------------------------
        # PROPAGATE KNOWN APPLICATION ERRORS
        # --------------------------------------------------------

        except AppException:
            logger.exception("Error in register account")
            raise

        # --------------------------------------------------------
        # HANDLE UNEXPECTED ERRORS
        # --------------------------------------------------------

        except Exception as exception:
            logger.exception("Error in register user")

            raise ProcessingException(
                message="Unable to complete account registration.",
                error_code=ErrorCode.AUTHENTICATION_PROCESSING_ERROR,
            ) from exception

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
        3. Verify that the account is not deleted.
        4. Retrieve the user's security state.
        5. Verify that the account is not locked.
        6. Verify the password.
        7. Register a failed attempt when authentication fails.
        8. Reset security state when authentication succeeds.
        9. Create an authenticated session.
        10. Generate authentication tokens.

        Known application exceptions are propagated unchanged.

        Unexpected exceptions are converted into a generic processing
        exception with an authentication-specific error code.
        """

        try:

            # ----------------------------------------------------
            # RETRIEVE USER
            # ----------------------------------------------------

            user = await (
                self.user_service.get_user_by_email(
                    payload.email
                )
            )

            # ----------------------------------------------------
            # PREVENT USER ENUMERATION
            # ----------------------------------------------------

            if user is None:

                # A dummy verification should still be performed
                # when the user does not exist. This helps reduce
                # observable timing differences between an unknown
                # email address and an incorrect password.

                self.password_service.verify_password(
                    payload.password,
                    self.user_security_service.dummy_password_hash,
                )

                raise InvalidCredentialsException()

            # ----------------------------------------------------
            # CHECK ACCOUNT STATUS
            # ----------------------------------------------------

            if not user.is_active:
                raise AccountInactiveException()

            # ----------------------------------------------------
            # CHECK SOFT DELETION
            # ----------------------------------------------------

            if user.deleted_at is not None:
                raise InvalidCredentialsException()

            # ----------------------------------------------------
            # RETRIEVE SECURITY STATE
            # ----------------------------------------------------

            security = await (
                self.user_security_service.get_security_by_user_id(
                    user.id
                )
            )

            # ----------------------------------------------------
            # CHECK ACCOUNT LOCK
            # ----------------------------------------------------

            if await (
                self.user_security_service.is_account_locked(
                    security
                )
            ):
                raise AccountLockedException()

            # ----------------------------------------------------
            # VERIFY PASSWORD
            # ----------------------------------------------------

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

                raise InvalidCredentialsException()

            # ----------------------------------------------------
            # HANDLE SUCCESSFUL LOGIN
            # ----------------------------------------------------

            await (
                self.user_security_service.handle_successful_login(
                    security
                )
            )

            # ----------------------------------------------------
            # CREATE AUTHENTICATED SESSION
            # ----------------------------------------------------

            session = await (
                self.user_session_service.create_session(
                    user_id=user.id,
                )
            )

            # ----------------------------------------------------
            # GENERATE ACCESS TOKEN
            # ----------------------------------------------------

            access_token = (
                self.jwt_manager_service.create_access_token(
                    user_id=user.id,
                    session_id=session.id,
                )
            )

            # ----------------------------------------------------
            # GENERATE REFRESH TOKEN
            # ----------------------------------------------------

            refresh_token = (
                self.jwt_manager_service.create_refresh_token(
                    user_id=user.id,
                    session_id=session.id,
                )
            )

            # ----------------------------------------------------
            # RETURN AUTHENTICATION RESPONSE
            # ----------------------------------------------------

            return AuthResponseDTO(
                user_id=user.id,
                email=user.email,
                access_token=access_token,
                refresh_token=refresh_token,
            )

        # --------------------------------------------------------
        # PROPAGATE KNOWN APPLICATION ERRORS
        # --------------------------------------------------------

        except AppException:
            logger.exception("Error in login user")
            raise

        # --------------------------------------------------------
        # HANDLE UNEXPECTED ERRORS
        # --------------------------------------------------------

        except Exception as exception:
            logger.exception("Error in login user")

            raise ProcessingException(
                message="Unable to complete user authentication.",
                error_code=ErrorCode.AUTHENTICATION_PROCESSING_ERROR,
            ) from exception