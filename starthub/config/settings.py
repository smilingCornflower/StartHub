import os
import sys
from pathlib import Path
from typing import Any, Mapping

from dotenv import load_dotenv
from loguru import logger

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = "../.env"

load_dotenv(BASE_DIR / ENV_FILE)

google_cloud_credentials_path = BASE_DIR / "../starthub-bucket-credentials.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(google_cloud_credentials_path)

# =====================================================================================================================
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
# =====================================================================================================================
_mode = os.getenv("MODE")
_secret_key = os.getenv("DJANGO_SECRET_KEY")
_debug = os.getenv("DEBUG")
_db_name = os.getenv("DB_NAME")
_db_user = os.getenv("DB_USER")
_db_password = os.getenv("DB_PASSWORD")
_db_host = os.getenv("DB_HOST")
_db_port = os.getenv("DB_PORT")
_allowed_hosts = os.getenv("ALLOWED_HOSTS")
_csrf_trusted_origins = os.getenv("CSRF_TRUSTED_ORIGINS")
_google_cloud_bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET_NAME")

if not (
    _mode
    and _secret_key
    and _debug
    and _db_name
    and _db_user
    and _db_password
    and _db_host
    and _db_port
    and _allowed_hosts
    and _csrf_trusted_origins
    and _google_cloud_bucket_name
):
    logger.warning(f"{bool(_mode)=}")
    logger.warning(f"{bool(_secret_key)=}")
    logger.warning(f"{bool(_debug)=}")
    logger.warning(f"{bool(_db_name)=}")
    logger.warning(f"{bool(_db_user)=}")
    logger.warning(f"{bool(_db_password)=}")
    logger.warning(f"{bool(_db_host)=}")
    logger.warning(f"{bool(_db_port)=}")
    logger.warning(f"{bool(_allowed_hosts)=}")
    logger.warning(f"{bool(_csrf_trusted_origins)=}")
    logger.warning(f"{bool(_google_cloud_bucket_name)=}")

    raise ValueError("Missing required environment variables.")
else:
    MODE: str = _mode.lower()
    SECRET_KEY: str = _secret_key
    DEBUG: bool = _debug.lower() == "true"
    DB_NAME: str = _db_name
    DB_USER: str = _db_user
    DB_PASSWORD: str = _db_password
    DB_HOST: str = _db_host
    DB_PORT: str = _db_port
    ALLOWED_HOSTS: list[str] = _allowed_hosts.split(",")
    CSRF_TRUSTED_ORIGINS: list[str] = _csrf_trusted_origins.split(",")
    GOOGLE_CLOUD_BUCKET_NAME: str = _google_cloud_bucket_name
logger.warning(f"{DEBUG=}")
# =====================================================================================================================

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
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "domain.User"
