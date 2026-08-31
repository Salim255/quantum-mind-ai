from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from starlette.responses import JSONResponse

from app.core.exceptions.custom_exceptions import (
    ProcessingException,
    UnauthorizedException,
)

from app.core.security.services.cookie_service import (
    CookieService,
)

from app.core.security.services.jwt_manager_service import (
    JWTManagerService,
)


class AuthenticationMiddleware:
    """
    Global authentication middleware.

    This middleware is executed before the request reaches
    the FastAPI router/controller.

    Its responsibility is to provide the application's
    global authentication gate.

    Request flow:

        Client
          │
          ▼
        Middleware
          │
          ├── Public route ───────────────► Controller
          │
          └── Protected route
                    │
                    ├── No token ─────────► 401
                    │
                    ├── Invalid token ────► 401
                    │
                    └── Valid token ──────► Controller


    The middleware is responsible only for authentication.

    It does NOT:

    - authenticate credentials during login
    - register users
    - create users
    - create sessions
    - issue tokens
    - refresh tokens
    - manage passwords
    - perform authorization
    - contain JWT cryptographic implementation

    Those responsibilities belong to the appropriate services.
    """

    def __init__(
        self,
        app,
        cookie_service: CookieService,
        jwt_manager_service: JWTManagerService,
    ) -> None:
        """
        Initializes the authentication middleware.

        Args:
            app:
                The next ASGI application in the middleware
                pipeline.

            cookie_service:
                Responsible for reading authentication cookies.

            jwt_manager_service:
                Responsible for validating JWT access tokens.
        """

        self.app = app
        self.cookie_service = cookie_service
        self.jwt_manager_service = jwt_manager_service

    # ============================================================
    # ASGI ENTRY POINT
    # ============================================================

    async def __call__(
        self,
        scope,
        receive,
        send,
    ) -> None:
        """
        Processes every incoming ASGI request.

        This method runs before the request reaches the
        FastAPI endpoint.

        The middleware therefore has the ability to stop
        unauthorized requests before the controller executes.
        """

        # ========================================================
        # NON-HTTP REQUESTS
        # ========================================================

        # Authentication is currently designed for HTTP requests.
        #
        # ASGI can also carry other connection types such as
        # WebSocket connections.
        #
        # We therefore allow non-HTTP traffic to continue without
        # applying HTTP authentication logic here.
        if scope["type"] != "http":
            await self.app(
                scope,
                receive,
                send,
            )
            return

        # ========================================================
        # CREATE REQUEST OBJECT
        # ========================================================

        # At the ASGI middleware level we receive:
        #
        #     scope
        #     receive
        #     send
        #
        # FastAPI's normal Request object has not been created
        # for us yet.
        #
        # We therefore create it manually so that our application
        # services can use the normal Request abstraction.
        request = Request(
            scope,
            receive=receive,
        )

        # ========================================================
        # PUBLIC ROUTE CHECK
        # ========================================================

        try:
            # ----------------------------------------------------
            # DETERMINE WHETHER ROUTE IS PUBLIC
            # ----------------------------------------------------

            is_public = self._is_public_route(
                request,
            )

            # ----------------------------------------------------
            # PUBLIC REQUEST
            # ----------------------------------------------------

            if is_public:

                # The endpoint explicitly allows anonymous access.
                #
                # Authentication must therefore be completely
                # skipped.
                #
                # We forward the ORIGINAL ASGI request unchanged.
                await self.app(
                    scope,
                    receive,
                    send,
                )

                return

        except Exception as exc:

            # ----------------------------------------------------
            # PUBLIC ROUTE DETECTION FAILURE
            # ----------------------------------------------------

            # If the middleware cannot determine whether an
            # endpoint is public, we must NOT accidentally allow
            # the request through.
            #
            # This is a security-sensitive operation, therefore
            # we fail closed.
            #
            # The original exception is preserved as the cause
            # for internal logging/debugging.
            error = ProcessingException(
                message=(
                    "Unable to determine route "
                    "authentication status."
                ),
            )

            await self._send_exception_response(
                send=send,
                exception=error,
            )

            return

        # ========================================================
        # PROTECTED ROUTE AUTHENTICATION
        # ========================================================

        try:

            # ----------------------------------------------------
            # GET ACCESS TOKEN
            # ----------------------------------------------------

            # The access token is stored inside the HttpOnly
            # authentication cookie.
            #
            # CookieService owns the cookie implementation.
            #
            # The middleware therefore does not know:
            #
            # - cookie configuration
            # - cookie names
            # - security attributes
            # - SameSite configuration
            #
            # It simply asks the service for the token.
            access_token = self.cookie_service.get_access_token(
                request=request,
            )

            # ----------------------------------------------------
            # TOKEN DOES NOT EXIST
            # ----------------------------------------------------

            if access_token is None:

                raise UnauthorizedException(
                    message="Authentication required.",
                )

            # ----------------------------------------------------
            # VERIFY ACCESS TOKEN
            # ----------------------------------------------------

            # JWTManagerService owns JWT validation.
            #
            # The manager is responsible for validating:
            #
            # - signature
            # - expiration
            # - JWT structure
            # - algorithm
            # - token claims required by the implementation
            #
            # If the token is invalid, the service raises the
            # appropriate authentication exception.
            self.jwt_manager_service.verify_access_token(
                access_token,
            )

        except UnauthorizedException as exc:

            # ====================================================
            # EXPECTED AUTHENTICATION FAILURE
            # ====================================================

            # This is NOT a server error.
            #
            # The client simply failed authentication.
            #
            # Because this exception happens inside middleware,
            # it cannot rely on FastAPI's normal endpoint
            # exception handling mechanism.
            #
            # We therefore convert it directly into the HTTP
            # response here.
            await self._send_exception_response(
                send=send,
                exception=exc,
            )

            return

        except Exception as exc:

            # ====================================================
            # UNEXPECTED AUTHENTICATION FAILURE
            # ====================================================

            # Any unexpected exception must NOT expose internal
            # implementation details to the client.
            #
            # Convert it into the application's generic
            # processing exception.
            error = ProcessingException(
                message="Unable to process authentication request.",
            )

            # The original exception remains available through
            # exception chaining for internal logging/debugging.
            error.__cause__ = exc

            await self._send_exception_response(
                send=send,
                exception=error,
            )

            return

        # ========================================================
        # AUTHENTICATION SUCCESSFUL
        # ========================================================

        # If execution reaches this point:
        #
        # - the route is protected
        # - an access token exists
        # - the access token was successfully verified
        #
        # The request is therefore authenticated.
        #
        # We now allow it to continue to FastAPI's router,
        # dependency system and finally the controller.
        await self.app(
            scope,
            receive,
            send,
        )

    # ============================================================
    # PUBLIC ROUTE DETECTION
    # ============================================================

    def _is_public_route(
        self,
        request: Request,
    ) -> bool:
        """
        Determines whether the requested endpoint is public.

        This method should use the application's route metadata
        mechanism rather than a hard-coded URL list.

        For example, an endpoint can eventually be declared as:

            @public_route
            @router.post("/login")
            async def login(...):
                ...

        The middleware then reads that metadata and decides
        whether authentication should be skipped.
        """

        return False

    # ============================================================
    # EXCEPTION RESPONSE
    # ============================================================

    async def _send_exception_response(
        self,
        send,
        exception: ProcessingException | UnauthorizedException,
    ) -> None:
        """
        Sends an application exception as an HTTP response.

        IMPORTANT:

        Middleware executes outside the normal FastAPI endpoint
        execution flow.

        Therefore an exception raised here cannot be assumed to
        reach the application's normal FastAPI exception handler.

        This method converts our application exception into the
        HTTP response directly.

        The response structure should match the structure used by
        the application's global exception handler.
        """

        # --------------------------------------------------------
        # BUILD RESPONSE BODY
        # --------------------------------------------------------

        body = {
            "success": False,
            "message": exception.message,
            "error_code": exception.error_code.value,
            "data": None,
        }

        # --------------------------------------------------------
        # SEND HTTP RESPONSE START
        # --------------------------------------------------------

        await send(
            {
                "type": "http.response.start",
                "status": exception.status_code,
                "headers": [
                    (
                        b"content-type",
                        b"application/json",
                    ),
                ],
            }
        )

        # --------------------------------------------------------
        # SEND HTTP RESPONSE BODY
        # --------------------------------------------------------

        import json

        await send(
            {
                "type": "http.response.body",
                "body": json.dumps(body).encode("utf-8"),
            }
        )