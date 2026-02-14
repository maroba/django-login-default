from django.views.generic import TemplateView

from .mixins import NoLoginRequiredMixin


class IndexView(NoLoginRequiredMixin, TemplateView):
    template_name = "django_login_default/index.html"


class DashboardView(TemplateView):
    template_name = "django_login_default/dashboard.html"


class PublicView(NoLoginRequiredMixin, TemplateView):
    template_name = "django_login_default/public.html"
