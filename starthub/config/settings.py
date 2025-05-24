import os
import sys
from pathlib import Path
from typing import Any, Mapping

from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = "../.env"

load_dotenv(BASE_DIR / ENV_FILE)

SECRET_KEY: str | None = os.getenv("DJANGO_SECRET_KEY")

if SECRET_KEY is None:
    raise ValueError("SECRET_KEY variable is not set.")

DEBUG = bool(os.getenv("DEBUG", default=0))

ALLOWED_HOSTS: list[str] = []
CSRF_TRUSTED_ORIGINS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "domain",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DB_NAME: str | None = os.getenv("DB_NAME")
DB_USER: str | None = os.getenv("DB_USER")
DB_PASSWORD: str | None = os.getenv("DB_PASSWORD")
DB_HOST: str | None = os.getenv("DB_HOST")
DB_PORT: str | None = os.getenv("DB_PORT")

if not (DB_USER and DB_NAME and DB_PASSWORD and DB_HOST and DB_PORT):
    raise ValueError("Missing required environment variables.")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
    }
}
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# =================================================================================================
AUTH_USER_MODEL = "domain.User"

# Logger
########################
# LOGURU CONFIGURATION #
########################
LOGURU_LOG_LEVEL: str | None = os.getenv("LOGURU_LOG_LEVEL")

if LOGURU_LOG_LEVEL is None:
    raise RuntimeError("LOGURU_LOG_LEVEL env var is not set")


def format_record(record: Mapping[str, Any]) -> str:
    record["extra"]["rel_path"] = Path(record["file"].path).relative_to(BASE_DIR)
    result = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level:<8}</level> | "
        "<cyan>{extra[rel_path]}</cyan>[<cyan>{line}</cyan>] "
        "(<cyan>{function}</cyan>) ----> <level>{message}</level>\n"
    )
    return result


logger.remove()

logger.add(
    sys.stdout,
    format=format_record,
    level=LOGURU_LOG_LEVEL,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)
