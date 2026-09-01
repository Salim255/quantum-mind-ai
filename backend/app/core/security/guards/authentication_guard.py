# app/core/security/guards/authentication_guard.py

from fastapi import Request

from app.core.exceptions.custom_exceptions import (
    UnauthorizedException,
)

from app.core.security.services.cookie_service import (
    CookieService,
)

from app.core.security.services.jwt_manager_service import (
    JWTManagerService,
)


class AuthenticationGuard:
    """
    Authentication guard responsible for protecting HTTP endpoints.

    The guard receives the security services it requires during
    construction.

    Dependency composition is handled outside the guard by the
    authentication dependency.

    The guard itself is responsible only for authenticating the
    current HTTP request.

    It does not:

    - create or resolve dependencies
    - access the application container
    - register users
    - log users in
    - create users
    - create sessions
    - issue tokens
    - refresh tokens
    - manage passwords
    - perform authorization
    - implement cookie handling
    - implement JWT validation
    """

    # ============================================================
    # INITIALIZATION
    # ============================================================

    def __init__(
        self,
        cookie_service: CookieService,
        jwt_manager_service: JWTManagerService,
    ) -> None:
        """
        Initializes the authentication guard.

        The required security services are injected by the
        composition layer.

        Args:
            cookie_service:
                Service responsible for reading the authentication
                access-token cookie.

            jwt_manager_service:
                Service responsible for validating the access token.
        """

        self.cookie_service = cookie_service
        self.jwt_manager_service = jwt_manager_service

    # ============================================================
    # AUTHENTICATE REQUEST
    # ============================================================

    async def __call__(
        self,
        request: Request,
    ) -> None:
        """
        Authenticates the current HTTP request.

        Authentication flow:

            Request
                │
                ▼
            Access-token cookie
                │
                ├── Missing ──────► UnauthorizedException
                │
                ▼
            Verify access token
                │
                ├── Invalid ──────► UnauthorizedException
                │
                └── Valid
                     │
                     ▼
                  Endpoint

        The guard does not return the authenticated user.

        Successful authentication is represented by the absence
        of an authentication exception. FastAPI can therefore
        continue with the remaining dependencies and endpoint.
        """

        # ========================================================
        # GET ACCESS TOKEN
        # ========================================================

        # CookieService owns all cookie-related implementation
        # details.
        #
        # The guard only asks the service for the access token.
        access_token = self.cookie_service.get_access_token(
            request=request,
        )

        # ========================================================
        # TOKEN REQUIRED
        # ========================================================


        print("Hello from contolre auth✅✅✅", access_token)
        # A protected endpoint requires a valid access token.
        if access_token is None:
            raise UnauthorizedException(
                message="Authentication required.",
            )

        # ========================================================
        # VERIFY ACCESS TOKEN
        # ========================================================

        # JWTManagerService owns all JWT validation logic.
        #
        # The guard does not know how the JWT is decoded,
        # verified, or validated.
        self.jwt_manager_service.verify_access_token(
            access_token,
        )

        # ========================================================
        # AUTHENTICATION SUCCESSFUL
        # ========================================================

        # No exception means authentication succeeded.
        #
        # FastAPI will continue with the request lifecycle and
        # eventually execute the endpoint.
        return