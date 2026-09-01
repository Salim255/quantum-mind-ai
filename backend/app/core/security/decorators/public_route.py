from collections.abc import Callable


def is_public(
    func: Callable,
) -> Callable:
    """
    Marks a FastAPI endpoint as publicly accessible.

    This decorator does not perform authentication.

    Its only responsibility is to attach metadata to the
    endpoint function indicating that authentication should
    be skipped for that endpoint.

    The AuthenticationMiddleware is responsible for reading
    this metadata through the application's public-route
    registry.

    Example:

        @auth_router.post("/register")
        @is_public
        async def register(...):
            ...

    The decorator adds:

        __public_route__ = True

    to the original endpoint function.

    This is intentionally implemented without wrapping the
    endpoint because FastAPI needs to keep the original
    endpoint function and its metadata intact.
    """

    # ========================================================
    # PUBLIC ROUTE METADATA
    # ========================================================

    # Mark the original FastAPI endpoint as public.
    #
    # True:
    #     AuthenticationMiddleware must allow the request
    #     without requiring an access token.
    #
    # Missing / False:
    #     The endpoint is considered protected.
    func.__public_route__ = True

    return func