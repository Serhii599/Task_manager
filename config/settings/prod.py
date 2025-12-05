from .docker import *

DEBUG = False

ALLOWED_HOSTS = ["*", "13.60.12.128", "localhost"]

STATIC_URL = "/static/"
STATIC_ROOT = "/static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/media/"

CSRF_TRUSTED_ORIGINS = ["http://13.60.12.128", "https://13.60.12.128"]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}