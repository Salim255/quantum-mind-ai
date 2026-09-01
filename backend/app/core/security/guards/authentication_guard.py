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

    The guard is responsible only for:

    - retrieving the access token
    - authenticating the token
    - establishing the authenticated user's identity
      for the current request

    Once authentication succeeds, the authenticated user's ID
    is stored in:

        request.state.user_id

    This allows downstream controllers and dependencies to
    access the authenticated identity without decoding the JWT
    again.

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
                Service responsible for validating the access token
                and returning its trusted claims.
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
                ▼
            Extract authenticated user ID
                │
                ▼
            request.state.user_id
                │
                ▼
            Controller

        The guard does not return the authenticated user.

        Instead, once the token has been successfully verified,
        the authenticated user's ID is attached to the current
        request through request.state.
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
        # The service verifies the token and returns the trusted
        # claims extracted from it.
        claims = self.jwt_manager_service.verify_access_token(
            access_token,
        )

        # ========================================================
        # ESTABLISH REQUEST IDENTITY
        # ========================================================

        # The user ID comes exclusively from the verified JWT.
        #
        # request.state is request-scoped storage provided by
        # Starlette/FastAPI.
        #
        # Downstream code can access the authenticated identity
        # through:
        #
        #     request.state.user_id
        #
        # No JWT decoding is required again.
      
        request.state.user_id = claims.get("sub")

        # ========================================================
        # AUTHENTICATION SUCCESSFUL
        # ========================================================

        # No exception means authentication succeeded.
        #
        # FastAPI continues with the remaining dependencies and
        # eventually executes the protected endpoint.
        return