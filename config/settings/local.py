# config/settings/local.py

from decouple import Csv, config

from .base import *

# Ative o modo debug para desenvolvimento
DEBUG = True

# Hosts permitidos em dev (runserver)
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",  # nome da variável no .env
    default="localhost,127.0.0.1",
    cast=Csv(),  # converte CSV em lista de strings
)

# Chave secreta só para dev (no prod leia de env var)
SECRET_KEY = config("SECRET_KEY")

# Se desejar usar sqlite em dev, pode manter o DATABASES do base
# ou sobrescrever aqui:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

# Opcional: logs mais verbosos em dev
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
