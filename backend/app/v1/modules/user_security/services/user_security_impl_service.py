import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID
from app.common.constants import (MAX_FAILED_LOGIN_ATTEMPTS, LOCK_DURATION_MINUTES)
from app.core.exceptions.base_exception import AppException
from app.core.exceptions.custom_exceptions import ProcessingException
from app.v1.modules.user_security.dto.user_security_dto import (
    UserSecurityDTO,
)
from app.v1.modules.user_security.models.user_security import (
    UserSecurity,
)
from app.v1.modules.user_security.repositories.user_security_repository import (
    UserSecurityRepository,
)
from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)


logger = logging.getLogger(__name__)


class UserSecurityImplService(UserSecurityService):
    """
    Concrete implementation of the user security service.

    UserSecurityImplService manages the persistent security state
    associated with user accounts.

    Its responsibility is limited to security-state management.

    It coordinates:

    - UserSecurityRepository
    - login-attempt tracking
    - account-lock evaluation
    - successful-login state reset
    - security metadata updates

    It does not manage:

    - User creation or retrieval
    - password hashing or verification
    - authentication tokens
    - sessions
    - cookies
    - profile information

    Higher-level authentication workflows are orchestrated by
    AuthImplService.

    Unexpected infrastructure or implementation errors are logged
    internally and converted into the shared ProcessingException so
    internal exception details are never exposed to API clients.
    """

   
    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        user_security_repository: UserSecurityRepository,
    ) -> None:
        """
        Initializes the user security service.

        UserSecurityRepository:
            Provides persistence operations for UserSecurity records.

        Security policy values are defined by the service because
        they represent application-level authentication protection
        rules rather than persistence concerns.
        """

        self.user_security_repository = (
            user_security_repository
        )
        
        self.MAX_FAILED_LOGIN_ATTEMPTS = MAX_FAILED_LOGIN_ATTEMPTS
        
        self.LOCK_DURATION_MINUTES = LOCK_DURATION_MINUTES
   

    # ============================================================
    # CREATE SECURITY
    # ============================================================

    async def create_security(
        self,
        user_id: UUID,
    ) -> UserSecurityDTO:
        """
        Creates the initial security state for a user.

        A new security record is initialized with safe default
        authentication-security values.

        The operation does not create or modify the User itself.
        """

        try:

            # ----------------------------------------------------
            # CREATE SECURITY RECORD
            # ----------------------------------------------------

            security = UserSecurity(
                user_id=user_id,
            )

            # ----------------------------------------------------
            # PERSIST SECURITY STATE
            # ----------------------------------------------------

            security = await (
                self.user_security_repository.create(
                    security
                )
            )

            # ----------------------------------------------------
            # RETURN SECURITY DTO
            # ----------------------------------------------------

            return UserSecurityDTO.model_validate(
                security
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in creating user security"
            )

            raise ProcessingException(
                message="Unable to create user security.",
            ) from exception

    # ============================================================
    # GET SECURITY
    # ============================================================

    async def get_security_by_user_id(
        self,
        user_id: UUID,
    ) -> UserSecurityDTO:
        """
        Retrieves the security record associated with a user.

        The user identifier is the lookup key because the relationship
        between User and UserSecurity is one-to-one.
        """

        try:

            # ----------------------------------------------------
            # RETRIEVE SECURITY RECORD
            # ----------------------------------------------------

            security = await (
                self.user_security_repository.get_by_user_id(
                    user_id
                )
            )

            if security is None:
                raise ProcessingException(
                    message="Unable to retrieve user security.",
                )

            # ----------------------------------------------------
            # RETURN SECURITY DTO
            # ----------------------------------------------------

            return UserSecurityDTO.model_validate(
                security
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in getting user security by user id"
            )

            raise ProcessingException(
                message="Unable to retrieve user security.",
            ) from exception

    # ============================================================
    # CHECK ACCOUNT LOCK
    # ============================================================

    async def is_account_locked(
        self,
        security: UserSecurityDTO,
    ) -> bool:
        """
        Determines whether the supplied security state currently
        prevents authentication.

        A lock is active only when `locked_until` exists and is
        later than the current UTC timestamp.

        Expired locks are therefore treated as inactive.
        """

        try:

            # ----------------------------------------------------
            # NO LOCK
            # ----------------------------------------------------

            if security.locked_until is None:
                return False

            # ----------------------------------------------------
            # CHECK LOCK EXPIRATION
            # ----------------------------------------------------

            now = datetime.now(UTC)

            return security.locked_until > now

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in checking account lock"
            )

            raise ProcessingException(
                message="Unable to determine account lock status.",
            ) from exception

    # ============================================================
    # HANDLE FAILED LOGIN
    # ============================================================

    async def handle_failed_login(
        self,
        security: UserSecurityDTO,
    ) -> UserSecurityDTO:
        """
        Records a failed authentication attempt.

        The failure counter is incremented and the timestamp of the
        failed attempt is updated.

        Once the configured threshold is reached, the account is
        temporarily locked.

        The lock policy is intentionally centralized here so that
        authentication workflows do not need to know how login
        protection is implemented.
        """

        try:

            # ----------------------------------------------------
            # UPDATE FAILURE STATE
            # ----------------------------------------------------

            failed_attempts = (
                security.failed_login_attempts + 1
            )

            now = datetime.now(UTC)

            # ----------------------------------------------------
            # BUILD UPDATE VALUES
            # ----------------------------------------------------

            update_data = {
                "failed_login_attempts": failed_attempts,
                "last_failed_login_at": now,
                "updated_at": now,
            }

            # ----------------------------------------------------
            # APPLY ACCOUNT LOCK
            # ----------------------------------------------------

            if (
                failed_attempts
                >= self.MAX_FAILED_LOGIN_ATTEMPTS
            ):
                update_data["locked_until"] = (
                    now
                    + timedelta(
                        minutes=self.LOCK_DURATION_MINUTES
                    )
                )

            # ----------------------------------------------------
            # PERSIST SECURITY STATE
            # ----------------------------------------------------

            updated_security = await (
                self.user_security_repository.update(
                    security.id,
                    update_data,
                )
            )

            # ----------------------------------------------------
            # RETURN UPDATED SECURITY STATE
            # ----------------------------------------------------

            return UserSecurityDTO.model_validate(
                updated_security
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in handling failed login"
            )

            raise ProcessingException(
                message="Unable to process failed login.",
            ) from exception

    # ============================================================
    # HANDLE SUCCESSFUL LOGIN
    # ============================================================

    async def handle_successful_login(
        self,
        security: UserSecurityDTO,
    ) -> UserSecurityDTO:
        """
        Updates the security state after successful authentication.

        A successful login:

        - resets consecutive failed login attempts
        - removes any active lock
        - records the successful login timestamp
        - updates the security audit timestamp

        Resetting the failed-attempt counter ensures that only
        consecutive authentication failures contribute toward
        account lockout.
        """

        try:

            # ----------------------------------------------------
            # CURRENT UTC TIME
            # ----------------------------------------------------

            now = datetime.now(UTC)

            # ----------------------------------------------------
            # RESET LOGIN PROTECTION STATE
            # ----------------------------------------------------

            update_data = {
                "failed_login_attempts": 0,
                "locked_until": None,
                "last_login_at": now,
                "updated_at": now,
            }

            # ----------------------------------------------------
            # PERSIST SECURITY STATE
            # ----------------------------------------------------

            updated_security = await (
                self.user_security_repository.update(
                    security.id,
                    update_data,
                )
            )

            # ----------------------------------------------------
            # RETURN UPDATED SECURITY STATE
            # ----------------------------------------------------

            return UserSecurityDTO.model_validate(
                updated_security
            )

        except AppException:
            raise

        except Exception as exception:
            logger.exception(
                "Error in handling successful login"
            )

            raise ProcessingException(
                message="Unable to process successful login.",
            ) from exception