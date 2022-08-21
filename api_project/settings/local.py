# noinspection PyUnresolvedReferences
from .base import *
from .base import env

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-(e=^s)6p5zxns1%+2mwfzfudg+$lp^w_=9cutvc&flr(m7*j=o",
)

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0"]

EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="mailhog")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "Share-gist Info <sgi.com>"
DOMAIN = env("DOMAIN")
SITE_NAME = "Share Gist"
