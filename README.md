# django-login-default

A Django middleware that makes login required the default. Instead of decorating
every view with `@login_required`, you add one middleware and then mark the
exceptions — the views that should be public.

Requires Django 4.2+ and Python 3.10+.

## Installation

```bash
pip install django-login-default
```

## Usage

### 1. Add the middleware

In your `settings.py`, add `LoginRequiredMiddleware` **after**
`AuthenticationMiddleware`:

```python
INSTALLED_APPS = [
    ...
    "django_login_default",
]

MIDDLEWARE = [
    ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_login_default.middleware.LoginRequiredMiddleware",
    ...
]

LOGIN_URL = "/accounts/login/"
```

That's it — every view now requires an authenticated user. Unauthenticated
requests get redirected to `LOGIN_URL` with a `?next=` parameter.

### 2. Mark public views

For views that should be accessible without login, use the decorator (FBV) or
the mixin (CBV):

```python
# Function-based view
from django_login_default.decorators import no_login_required

@no_login_required
def landing_page(request):
    ...
```

```python
# Class-based view
from django_login_default.mixins import NoLoginRequiredMixin

class LandingPage(NoLoginRequiredMixin, TemplateView):
    template_name = "landing.html"
```

### How it works

The middleware runs on every request. If the user is not authenticated, it
resolves the URL and checks the view for a `no_login_required` attribute. If
the attribute is present (set by the decorator or mixin), the request passes
through. Otherwise, it redirects to the login page.

---

## Development

### Setup

```bash
git clone https://github.com/mbaer/django-login-default.git
cd django-login-default
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Sample project

There's a small Django project in `sample_project/` that demonstrates the
middleware. It has a protected page, a public page, and a login form.

```bash
cd sample_project
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Running tests

```bash
# With coverage
PYTHONPATH=sample_project:$PYTHONPATH \
  coverage run --source=django_login_default -m django test django_login_default \
  --settings=sample_project.settings
coverage report

# Across multiple Python/Django versions
pip install tox
tox
```

### Project structure

```
django_login_default/
├── middleware.py      # LoginRequiredMiddleware
├── decorators.py      # @no_login_required
├── mixins.py          # NoLoginRequiredMixin
├── views.py           # Demo views used by the sample project
└── tests/
    └── test_middleware.py
```

## License

MIT
