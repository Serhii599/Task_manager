from .docker import *

DEBUG = False
ALLOWED_HOSTS = ["*"] 

STATIC_URL = "/static/"
STATIC_ROOT = "/app/staticfiles/"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/app/media/"