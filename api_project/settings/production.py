# noinspection PyUnresolvedReferences
# noinspection PyUnresolvedReferences
from .base import *
from .base import env

# SECRET_KEY = env("DJANGO_SECRET_KEY")
#
# ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["example.com"])
# ADMIN_URL = env("DJANGO_ADMIN_URL")
#
# DATABASES = {"default": env.db("DATABASE_URL")}
# DATABASES["default"]["ATOMIC_REQUESTS"] = True
#
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
#
# SECURE_SSL_REDIRECT = True
#
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
#
# SECURE_HSTS_SECONDS = 60
#
# SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=True)
#
# SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
#     "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
# )
#
DEFAULT_FROM_EMAIL = "Share-gist Info <sgi.com>"
