# Django Migrate Middleware

Run migrations on every request

## Install

```bash
pip install django-migrate-middleware
```

In the django settings file add package to the middleware settings.

```python
MIDDLEWARE = [
    "django_migrate_middleware.MigrateMiddleware",
  # ...
]
```
