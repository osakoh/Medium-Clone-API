from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()

# ROOT_DIR: ...\BlogAPI
# APPS_DIR: ...\BlogAPI\main_apps
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

APPS_DIR = ROOT_DIR / "main_apps"

# print(f"\n\n#######################################################################")
# print(f"ROOT_DIR: {ROOT_DIR}")
# print(f"APPS_DIR: {APPS_DIR}")
# print(f"#######################################################################\n\n")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)

DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "django_filters",
    "django_countries",
    "phonenumber_field",
    "drf_yasg",  # documentation
    "corsheaders",
    "djcelery_email",
    "djoser",
    "rest_framework_simplejwt",
    "haystack",
    "drf_haystack",
]

LOCAL_APPS = [
    "main_apps.core",
    "main_apps.common",
    "main_apps.profiles",
    "main_apps.articles",
    "main_apps.comments",
    "main_apps.favorites",
    "main_apps.ratings",
    "main_apps.reactions",
    "main_apps.search",
]

# Application definition
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    #  email errors about broken links (404 "page not found" errors)
    "django.middleware.common.BrokenLinkEmailsMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                # each RequestContext has access to LANGUAGES, LANGUAGE_CODE, and LANGUAGE_BIDI
                "django.template.context_processors.i18n",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# override default algorithm for storing passwords using Argon2
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",  # custom algorithm(Argon2) for storing passwords
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# British English
LANGUAGE_CODE = "en-gb"

TIME_ZONE = "Europe/London"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

ADMIN_URL = "controller/"

ADMINS = [("""Custom Admin""", "retry2067@gmail.com")]

# broken link notifications and other various emails
MANAGERS = ADMINS

# Subject-line prefix for email messages send with django.core.mail.mail_admins
# or ...mail_managers.  Make sure to include the trailing space.
EMAIL_SUBJECT_PREFIX = "[Share-gist Admin] "

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/staticfiles/"
# where static files are collected when 'manage.py collectstatic' is ran
STATIC_ROOT = str(ROOT_DIR / "staticfiles")
#  actual location of static files
STATICFILES_DIRS = []
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = str(ROOT_DIR / "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Useful when only CORS is needed on a part of your site, e.g. an API at /api/.
CORS_URLS_REGEX = r"^/api/.*$"

# use custom exception for DRF
REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "main_apps.common.exceptions.common_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

# djangorestframework-simplejwt config
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=720),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "SIGNING_KEY": env("SIGNING_KEY"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# DJOSER config
DJOSER = {
    "LOGIN_FIELD": "email",
    "USER_CREATE_PASSWORD_RETYPE": True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    "SEND_CONFIRMATION_EMAIL": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_RETYPE": True,
    "USERNAME_RESET_CONFIRM_RETYPE": "email/reset/confirm/{uid}/{token}",
    "ACTIVATION_URL": "activate/{uid}/{token}",
    "SEND_ACTIVATION_EMAIL": True,
    "SERIALIZERS": {
        "user_create": "main_apps.core.serializers.CreateUserSerializer",
        "user": "main_apps.core.serializers.UserSerializer",
        "current_user": "main_apps.core.serializers.UserSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}

# custom user authentication model
AUTH_USER_MODEL = "core.User"

# celery and django celery results config
CELERY_BROKER_URL = env("CELERY_BROKER")
CELERY_RESULT_BACKEND = env("CELERY_BACKEND")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/London"

# |--------------------------------------------- Haystack Settings ---------------------------------------|
# HAYSTACK_CONNECTIONS: controls which backends should be available. This is required.
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack.backends.whoosh_backend.WhooshEngine",
        #  The filesystem path to where the index data is to be stored/located
        "PATH": ROOT_DIR / "whoosh_index",
    }
}

# This is an optional setting.
# Controls how many results are shown per page when using the included SearchView and its subclasses.
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

# This is an optional setting.
# Controls what SignalProcessor class is used to handle Django’s signals & keep the search index up-to-date.
# Enforces the real-time index as the database in being updated
HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
# |--------------------------------------------- Haystack Settings ---------------------------------------|

# logging settings
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "[%(name)-12s:line-%(lineno)d %(process)d %(thread)d] => %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}
