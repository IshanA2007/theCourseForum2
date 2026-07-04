"""Django settings for the Culprit fault-injection harness.

A production-faithful LOCAL profile. Unlike ``dev.py`` (runserver, DEBUG=True,
LocMemCache, cachalot OFF, no Redis) this mirrors the parts of ``prod.py`` that
make production faults reachable:

* ``DEBUG = False`` — real 500 pages, no debug toolbar, exceptions flow to the
  HandleExceptionsMiddleware (JSON->stderr) and to Sentry.
* Redis cache + ``cached_db`` sessions + ``CACHALOT_ENABLED = True`` — mirrors
  ``prod.py:50-66`` so the Redis-dependency and cache faults are exercisable.

Unlike ``prod.py`` it does NOT require the AWS_* / S3 / ELB / Cognito vars — it
runs against the local Postgres and a local Redis container, and serves static
from disk. Selected via ``DJANGO_SETTINGS_MODULE=tcf_core.settings.harness``.
"""

from .base import *  # noqa: F403

DEBUG = False

# The harness runs behind gunicorn on a local tunnel; host validation is not the
# thing under test here.
ALLOWED_HOSTS = ["*"]

# Local Postgres (the harness's own throwaway db container — reset per scenario
# from db/local.dump). Same DB_* env names the dev profile uses.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DB_NAME"),  # noqa: F405
        "USER": env.str("DB_USER"),  # noqa: F405
        "PASSWORD": env.str("DB_PASSWORD"),  # noqa: F405
        "HOST": env.str("DB_HOST", default="db"),  # noqa: F405
        "PORT": env.int("DB_PORT", default=5432),  # noqa: F405
    }
}

# Static served from disk (no S3). DEBUG=False means Django won't serve static
# itself, but the harness only needs pages to RENDER (HTML) to trigger faults;
# missing CSS is cosmetic. collectstatic writes here (release task).
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa: F405

# Redis cache + cached_db sessions + cachalot ON — mirrors prod.py:50-66 so the
# unguarded-Redis-dependency faults (RECON #1) are reachable.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": env.str("REDIS_URL", default="redis://culprit_redis:6379"),  # noqa: F405
        "KEY_PREFIX": "tcf:harness",
        "OPTIONS": {
            "socket_connect_timeout": 5,
            "socket_timeout": 5,
            "retry_on_timeout": True,
        },
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"

CACHALOT_ENABLED = True
CACHALOT_TIMEOUT = 60 * 60 * 24 * 7  # 1 week, matching prod

# Sentry — DSN-gated, so this module is a no-op until the Sentry project exists
# (plan Task 4). release = the deploy-window HEAD SHA (decision 5): frequently a
# decoy, so `release` never functions as the eval answer key.
SENTRY_DSN = env.str("SENTRY_DSN", default="")  # noqa: F405
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        environment="fault-harness",
        release=env.str("SENTRY_RELEASE", default=None),  # noqa: F405
        traces_sample_rate=0.0,  # errors-only; protect the 5k/month free quota
        send_default_pii=True,
    )
