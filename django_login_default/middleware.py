from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve


class LoginRequiredMiddleware:
    """Redirect unauthenticated requests to the login URL.

    Every request by an unauthenticated user is redirected to
    ``settings.LOGIN_URL`` **unless** the resolved view is marked with
    the ``@no_login_required`` decorator or the ``NoLoginRequiredMixin``.

    Add to ``MIDDLEWARE`` **after**
    ``django.contrib.auth.middleware.AuthenticationMiddleware``.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            resolved = resolve(request.path)
            if not self._is_login_exempt(resolved):
                login_url = getattr(settings, "LOGIN_URL", "/accounts/login/")
                if request.path != login_url:
                    return redirect(f"{login_url}?next={request.path}")

        return self.get_response(request)

    @staticmethod
    def _is_login_exempt(resolved):
        """Return ``True`` when the view opts out of authentication."""
        view_func = resolved.func

        # Function-based views decorated with @no_login_required
        if getattr(view_func, "no_login_required", False):
            return True

        # Class-based views using NoLoginRequiredMixin
        view_class = getattr(view_func, "view_class", None)
        if view_class and getattr(view_class, "no_login_required", False):
            return True

        return False
