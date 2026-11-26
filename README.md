# django-axes: `from axes.conf import LockoutTier` in settings crashes Django

Minimal reproduction for https://github.com/django-commons/django-axes/issues/1544.

The [configuration docs](https://django-axes.readthedocs.io/en/latest/4_configuration.html)
show `AXES_LOCKOUT_TIERS` configured in `settings.py` with `from axes.conf import LockoutTier`.
Doing exactly that makes Django fail on startup, because none of axes' defaults end up in `django.conf.settings`.

## Reproduce

Requires [uv](https://docs.astral.sh/uv/).

```sh
uv run python manage.py check
```

```
AttributeError: 'Settings' object has no attribute 'AXES_VERBOSE'
```

Which `AXES_*` setting is reported missing depends on which code reads one first
(with `django.contrib.admin` installed it is `AXES_ACCESS_FAILURE_LOG_PER_USER_LIMIT`).
Defining that setting by hand only moves the error to the next one.

Removing the `axes.conf` import and `AXES_LOCKOUT_TIERS` from `reproproject/settings.py` makes `check` pass.

## Why

1. Django starts loading the settings module (`LazySettings._setup()` → `Settings(settings_module)` → `import_module(...)`).
2. The settings module imports `axes.conf`, which reads `settings.AXES_ENABLED` etc. at import time.
3. `_wrapped` is still unset, so Django runs `_setup()` again. `import_module` returns the half-executed
   settings module from `sys.modules`, and `_wrapped` is set to a `Settings` built from it.
4. `axes.conf` writes all its defaults into that `Settings` object.
5. The outer `Settings(...)` from step 1 finishes and `self._wrapped = Settings(settings_module)` replaces it,
   discarding every default axes set.

## Versions

- Python 3.14
- Django 6.0.9
- django-axes 9.1.0
