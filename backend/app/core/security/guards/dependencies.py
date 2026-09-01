from typing import Annotated
from fastapi import Request, Depends

from app.core.container import Container

from app.core.security.dependencies import (
    get_cookie_service,
    get_jwt_manager_service,
)

from app.core.security.guards.authentication_guard import (
    AuthenticationGuard,
)


# ============================================================
# CONTAINER DEPENDENCY
# ============================================================

def get_container(
    request: Request,
) -> Container:
    """
    Retrieves the application dependency container.

    The container is stored on FastAPI's application state.

    It provides access to application-wide infrastructure such as:

    - application settings
    - database session management
    - shared infrastructure services

    The controller is responsible for obtaining the container
    because it represents the outer application boundary.
    """

    return request.app.state.container

# ============================================================
# AUTHENTICATION GUARD
# ============================================================
# ============================================================
# AUTHENTICATION GUARD DEPENDENCY
# ============================================================

async def get_authentication_guard(
    request: Request,
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> None:
    """
    Authenticates the current HTTP request.

    This function is the FastAPI dependency boundary for the
    AuthenticationGuard.

    Its responsibilities are limited to:

    1. Obtaining the application container through FastAPI's
       dependency injection system.

    2. Creating the security services required by the guard:
           - CookieService
           - JWTManagerService

    3. Creating a fully configured AuthenticationGuard.

    4. Executing the guard for the current HTTP request.

    The dependency therefore handles dependency composition,
    while AuthenticationGuard remains responsible exclusively
    for authentication.

    Dependency flow:

        FastAPI
           │
           ▼
        get_container()
           │
           ▼
        Container
           │
           ├──────────────────────┐
           │                      │
           ▼                      ▼
    get_cookie_service()   get_jwt_manager_service()
           │                      │
           ▼                      ▼
    CookieService          JWTManagerService
           │                      │
           └──────────┬───────────┘
                      ▼
             AuthenticationGuard
                      │
                      ▼
              await guard(request)
                      │
                 ┌────┴────┐
                 │         │
              Invalid     Valid
                 │         │
                401     Continue
                           │
                           ▼
                       Endpoint

    Important:

    AuthenticationGuard does not:

    - access FastAPI's Request through dependency injection
    - access the application container
    - create its own dependencies
    - know about FastAPI's Depends mechanism

    All dependency resolution and composition happens here.

    The guard receives only the concrete service abstractions
    it needs and is then responsible for authenticating the
    current request.

    Args:
        request:
            The current HTTP request being authenticated.

        container:
            The shared application container resolved by FastAPI.
            It provides the application configuration required
            to construct the security services.
    """

    # ========================================================
    # SECURITY SERVICES
    # ========================================================

    # Create the cookie service from the shared application
    # container.
    #
    # CookieService is responsible for all authentication-cookie
    # operations. The guard does not need to know how cookies
    # are configured or read.
    cookie_service = get_cookie_service(
        container=container,
    )

    # Create the JWT manager from the same application container.
    #
    # JWTManagerService is responsible for all JWT operations,
    # including access-token validation. The guard delegates
    # JWT implementation details to this service.
    jwt_manager_service = get_jwt_manager_service(
        container=container,
    )

    # ========================================================
    # AUTHENTICATION GUARD
    # ========================================================

    # Compose the guard with the services it requires.
    #
    # The guard receives its dependencies explicitly and remains
    # completely independent from the application container and
    # FastAPI's dependency-injection system.
    guard = AuthenticationGuard(
        cookie_service=cookie_service,
        jwt_manager_service=jwt_manager_service,
    )

    # ========================================================
    # EXECUTE AUTHENTICATION
    # ========================================================

    # Execute authentication for the current request.
    #
    # If authentication fails, the guard raises the appropriate
    # authentication exception and FastAPI stops processing the
    # endpoint.
    #
    # If authentication succeeds, no exception is raised and
    # FastAPI continues with the remaining dependencies and
    # eventually executes the endpoint.
    await guard(
        request=request,
    )