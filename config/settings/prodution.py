# config/settings/production.py

from .base import *
import os
from decouple import config

# ------------------------------------------------------------------------------
# PRODUCTION SETTINGS
# ------------------------------------------------------------------------------
DEBUG = False

# Permite hosts definidos por variável de ambiente (ex.: "meu.domínio.com,www.domínio.com")
ALLOWED_HOSTS = config("ALLOWED_HOSTS")

# Chave secreta em variável de ambiente
SECRET_KEY = config("SECRET_KEY")

# ------------------------------------------------------------------------------
# DATABASE SETTINGS (exemplo com PostgreSQL)
# ------------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", "localhost"),
        "PORT": config("DB_PORT", "5432"),
    }
}

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ------------------------------------------------------------------------------
# STATIC & MEDIA
# ------------------------------------------------------------------------------
# Diretório de coleta estática
STATIC_ROOT = BASE_DIR / "staticfiles"
# Opcional: se usar CDN
# STATIC_URL = os.getenv("STATIC_URL", "/static/")

MEDIA_ROOT = BASE_DIR / "mediafiles"
MEDIA_URL = config("MEDIA_URL", "/media/")

# ------------------------------------------------------------------------------
# LOGGING (nível INFO em produção)
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
