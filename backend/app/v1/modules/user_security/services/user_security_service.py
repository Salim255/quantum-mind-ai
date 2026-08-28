from abc import ABC, abstractmethod
from uuid import UUID

from app.v1.modules.user_security.dto.user_security_dto import UserSecurityDTO


class UserSecurityService(ABC):
    """
    Defines the application-level user security contract.

    UserSecurityService is responsible for managing the persistent
    security state associated with a user account.

    The service owns security-state operations such as:

    - creating the initial security record
    - retrieving security state
    - determining whether an account is locked
    - recording failed login attempts
    - handling successful authentication
    - maintaining login-related security metadata

    Authentication orchestration remains the responsibility of
    AuthService.

    Password hashing and verification remain the responsibility of
    PasswordService.

    Session lifecycle remains the responsibility of
    UserSessionService.

    Controllers and higher-level application services should depend
    on this abstraction rather than on UserSecurityImplService.
    """

    # ============================================================
    # CREATE SECURITY
    # ============================================================

    @abstractmethod
    async def create_security(
        self,
        user_id: UUID,
    ) -> UserSecurityDTO:
        """
        Creates the initial security state for a user account.

        A security record is created when a new user account is
        registered.

        Initial security state includes values such as:

        - email_verified = False
        - failed_login_attempts = 0
        - locked_until = None
        - security_version = 0
        - mfa_enabled = False
        - compromised_at = None

        The user account itself is not created by this method.
        """

        raise NotImplementedError

    # ============================================================
    # GET SECURITY
    # ============================================================

    @abstractmethod
    async def get_security_by_user_id(
        self,
        user_id: UUID,
    ) -> UserSecurityDTO:
        """
        Retrieves the security state associated with a user.

        Each user has exactly one UserSecurity record.

        This method is used by authentication workflows to retrieve
        security information required to evaluate account access.

        The method must raise the appropriate application exception
        when the security record does not exist.
        """

        raise NotImplementedError

    # ============================================================
    # CHECK ACCOUNT LOCK
    # ============================================================

    @abstractmethod
    async def is_account_locked(
        self,
        security: UserSecurityDTO,
    ) -> bool:
        """
        Determines whether authentication is currently blocked
        for the account.

        The account is considered locked when its `locked_until`
        timestamp exists and is still in the future.

        An expired lock must no longer prevent authentication.

        This method evaluates security state only. It does not
        modify the account.
        """

        raise NotImplementedError

    # ============================================================
    # HANDLE FAILED LOGIN
    # ============================================================

    @abstractmethod
    async def handle_failed_login(
        self,
        security: UserSecurityDTO,
    ) -> UserSecurityDTO:
        """
        Records a failed authentication attempt.

        The security state is updated by:

        - incrementing failed_login_attempts
        - updating last_failed_login_at
        - applying the account-lock policy when the configured
          failure threshold is reached

        This method is responsible only for maintaining the
        persistent security state.

        Password validation itself remains outside this service.
        """

        raise NotImplementedError

    # ============================================================
    # HANDLE SUCCESSFUL LOGIN
    # ============================================================

    @abstractmethod
    async def handle_successful_login(
        self,
        security: UserSecurityDTO,
    ) -> UserSecurityDTO:
        """
        Updates security state after successful authentication.

        The successful-login workflow resets consecutive failed
        login attempts and removes any expired or active lock state.

        It also records the timestamp of the successful login.

        This method does not create a session or generate tokens.
        Those responsibilities belong to UserSessionService and
        JWTManagerService respectively.
        """

        raise NotImplementedError