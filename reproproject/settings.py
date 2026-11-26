from datetime import timedelta

# As shown in https://django-axes.readthedocs.io/en/latest/4_configuration.html
from axes.conf import LockoutTier

SECRET_KEY = "repro"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "axes",
]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

AXES_LOCKOUT_TIERS = [
    LockoutTier(failures=3, cooloff=timedelta(minutes=15)),
]
