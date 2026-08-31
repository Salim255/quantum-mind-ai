from functools import wraps


def public_route(func):
    """
    Marks an endpoint as publicly accessible.

    Endpoints marked with this decorator bypass the global
    authentication middleware.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.__public_route__ = True

    return wrapper