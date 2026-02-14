class NoLoginRequiredMixin:
    """Mark a class-based view as not requiring authentication.

    Add this mixin to a CBV to exempt it from the
    ``LoginRequiredMiddleware``.

    Example::

        class PublicPageView(NoLoginRequiredMixin, TemplateView):
            template_name = "public.html"
    """

    no_login_required = True
