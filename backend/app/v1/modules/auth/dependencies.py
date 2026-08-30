# app/v1/modules/auth/dependencies.py

from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.container import Container

from app.db.transactions.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)
from app.db.transactions.unit_of_work import UnitOfWork

from app.v1.modules.auth.services.auth_impl_service import (
    AuthImplService,
)
from app.v1.modules.auth.services.auth_service import (
    AuthService,
)

from app.v1.modules.auth.services.cookie_impl_service import (
    CookieImplService,
)
from app.v1.modules.auth.services.cookie_service import (
    CookieService,
)

from app.v1.modules.auth.services.jwt_manager_impl_service import (
    JWTManagerImplService,
)
from app.v1.modules.auth.services.jwt_manager_service import (
    JWTManagerService,
)

from app.v1.modules.auth.services.password_impl_service import (
    PasswordImplService,
)
from app.v1.modules.auth.services.password_service import (
    PasswordService,
)

from app.v1.modules.profile.dependencies import (
    get_profile_service,
)
from app.v1.modules.profile.services.profile_service import (
    ProfileService,
)

from app.v1.modules.user.dependencies import (
    get_user_service,
)
from app.v1.modules.user.services.user_service import (
    UserService,
)

from app.v1.modules.user_security.dependencies import (
    get_user_security_service,
)
from app.v1.modules.user_security.services.user_security_service import (
    UserSecurityService,
)

from app.v1.modules.user_session.dependencies import (
    get_user_session_service,
)
from app.v1.modules.user_session.services.user_session_service import (
    UserSessionService,
)


# ============================================================
# PASSWORD SERVICE
# ============================================================

def get_password_service() -> PasswordService:
    """
    Creates the password service.

    PasswordService does not require a database session because
    password hashing and verification are independent from
    database persistence.
    """

    return PasswordImplService()


# ============================================================
# JWT MANAGER SERVICE
# ============================================================

def get_jwt_manager_service(
    container: Container,
) -> JWTManagerService:
    """
    Creates the JWT manager service.

    JWTManagerService requires application settings but does
    not require a database session.

    The container is therefore used only for configuration.
    """

    return JWTManagerImplService(
        settings=container.settings,
    )


# ============================================================
# COOKIE SERVICE
# ============================================================

def get_cookie_service(
    container: Container,
) -> CookieService:
    """
    Creates the cookie service.

    CookieService requires application settings but does not
    require a database session.
    """

    return CookieImplService(
        settings=container.settings,
    )


# ============================================================
# UNIT OF WORK
# ============================================================

def get_unit_of_work(
    session: AsyncSession,
) -> UnitOfWork:
    """
    Creates the UnitOfWork from the provided database session.

    The UnitOfWork does NOT create its own session.

    The session comes from the caller, which means the UnitOfWork
    can participate in the exact same database transaction as
    all repositories used by AuthService.
    """

    return SQLAlchemyUnitOfWork(
        session=session,
    )


# ============================================================
# AUTH SERVICE
# ============================================================

def get_auth_service(
    session: AsyncSession,
    container: Container,
) -> AuthService:
    """
    Creates the authentication service.

    The database session is explicitly provided by the caller.

    This dependency does not obtain the database session itself.

    The same session is passed to every database-dependent
    service used by AuthService.

    Therefore:

        UserService
        ProfileService
        UserSecurityService
        UserSessionService
        UnitOfWork

    all operate on the same AsyncSession.

    This is what allows a registration workflow to be handled
    as one atomic database transaction.
    """

    # --------------------------------------------------------
    # DATABASE-DEPENDENT SERVICES
    # --------------------------------------------------------

    user_service: UserService = get_user_service(
        session=session,
    )

    profile_service: ProfileService = get_profile_service(
        session=session,
    )

    user_security_service: UserSecurityService = (
        get_user_security_service(
            session=session,
        )
    )

    user_session_service: UserSessionService = (
        get_user_session_service(
            session=session,
        )
    )

    # --------------------------------------------------------
    # UNIT OF WORK
    # --------------------------------------------------------

    # The UnitOfWork receives the SAME session as every
    # database-dependent service above.
    #
    # It therefore controls the transaction containing
    # all registration database operations.

    unit_of_work_service: UnitOfWork = get_unit_of_work(
        session=session,
    )

    # --------------------------------------------------------
    # NON-DATABASE SERVICES
    # --------------------------------------------------------

    password_service: PasswordService = (
        get_password_service()
    )

    jwt_manager_service: JWTManagerService = (
        get_jwt_manager_service(
            container=container,
        )
    )

    cookie_service: CookieService = (
        get_cookie_service(
            container=container,
        )
    )

    # --------------------------------------------------------
    # CREATE AUTH SERVICE
    # --------------------------------------------------------

    return AuthImplService(
        user_service=user_service,
        profile_service=profile_service,
        user_security_service=user_security_service,
        user_session_service=user_session_service,
        password_service=password_service,
        jwt_manager_service=jwt_manager_service,
        cookie_service=cookie_service,
        unit_of_work_service=unit_of_work_service,
    )