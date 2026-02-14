import functools


def no_login_required(view_func):
    """Mark a view function as not requiring authentication.

    Use this decorator on function-based views to exempt them from
    the ``LoginRequiredMiddleware``.

    Example::

        @no_login_required
        def public_page(request):
            ...
    """

    @functools.wraps(view_func)
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)

    wrapped_view.no_login_required = True
    return wrapped_view
