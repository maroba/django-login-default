from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.http import HttpResponse
from django.urls import path
from django.views.generic import TemplateView

from django_login_default.decorators import no_login_required
from django_login_default.middleware import LoginRequiredMiddleware
from django_login_default.mixins import NoLoginRequiredMixin

User = get_user_model()


# ---------------------------------------------------------------------------
# Dummy views used by tests
# ---------------------------------------------------------------------------


def protected_view(request):
    return HttpResponse("protected")


@no_login_required
def public_view(request):
    return HttpResponse("public")


class ProtectedCBV(TemplateView):
    template_name = "django_login_default/index.html"


class PublicCBV(NoLoginRequiredMixin, TemplateView):
    template_name = "django_login_default/index.html"


@no_login_required
def login_view(request):
    return HttpResponse("login")


urlpatterns = [
    path("protected/", protected_view, name="protected"),
    path("public/", public_view, name="public"),
    path("protected-cbv/", ProtectedCBV.as_view(), name="protected-cbv"),
    path("public-cbv/", PublicCBV.as_view(), name="public-cbv"),
    path("accounts/login/", login_view, name="login"),
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

LOGIN_URL = "/accounts/login/"


@override_settings(LOGIN_URL=LOGIN_URL, ROOT_URLCONF="django_login_default.tests.test_middleware")
class LoginRequiredMiddlewareTest(TestCase):
    """Tests for LoginRequiredMiddleware."""

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="testuser", password="secret")
        self.middleware = LoginRequiredMiddleware(lambda req: HttpResponse("ok"))

    # -- anonymous requests ------------------------------------------------

    def test_anonymous_redirected_from_protected_fbv(self):
        request = self.factory.get("/protected/")
        request.user = self._anonymous_user()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(LOGIN_URL, response.url)

    def test_anonymous_redirected_from_protected_cbv(self):
        request = self.factory.get("/protected-cbv/")
        request.user = self._anonymous_user()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(LOGIN_URL, response.url)

    def test_anonymous_allowed_on_decorated_fbv(self):
        request = self.factory.get("/public/")
        request.user = self._anonymous_user()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_allowed_on_mixin_cbv(self):
        request = self.factory.get("/public-cbv/")
        request.user = self._anonymous_user()
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_allowed_on_login_url(self):
        request = self.factory.get(LOGIN_URL)
        request.user = self._anonymous_user()
        response = self.middleware(request)
        # Should not cause a redirect loop
        self.assertEqual(response.status_code, 200)

    # -- authenticated requests -------------------------------------------

    def test_authenticated_passes_through(self):
        request = self.factory.get("/protected/")
        request.user = self.user
        response = self.middleware(request)
        self.assertEqual(response.status_code, 200)

    # -- redirect preserves next parameter --------------------------------

    def test_redirect_includes_next_parameter(self):
        request = self.factory.get("/protected/")
        request.user = self._anonymous_user()
        response = self.middleware(request)
        self.assertEqual(response.url, f"{LOGIN_URL}?next=/protected/")

    # -- helpers -----------------------------------------------------------

    @staticmethod
    def _anonymous_user():
        from django.contrib.auth.models import AnonymousUser

        return AnonymousUser()
