# app/core/security/dependencies.py

from app.core.container import Container

from app.core.security.services.cookie_service import CookieService
from app.core.security.services.jwt_manager_service import JWTManagerService

from app.core.security.services.cookie_impl_service import (
    CookieImplService,
)

from app.core.security.services.jwt_manager_impl_service import (
    JWTManagerImplService,
)


# ============================================================
# JWT MANAGER SERVICE
# ============================================================

def get_jwt_manager_service(
    container: Container,
) -> JWTManagerService:
    """
    Creates the JWT manager service.

    JWTManagerService requires only application configuration.
    It does not require:

    - a database session
    - a request
    - an endpoint dependency

    The container provides the application settings used by
    the concrete JWT implementation.
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

    CookieService requires only application configuration.
    It does not require:

    - a database session
    - a request
    - an endpoint dependency

    The container provides the application settings used by
    the concrete cookie implementation.
    """

    return CookieImplService(
        settings=container.settings,
    )