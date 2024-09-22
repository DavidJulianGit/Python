import environ

from .base import *

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(str(BASE_DIR / ".env"))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = ["recipe-app-production-5f88.up.railway.app"]
CSRF_TRUSTED_ORIGINS = [
    "https://recipe-app-production-5f88.up.railway.app"
]  # modify later

MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": env.str("DB_NAME"),
#         "USER": env.str("DB_USER"),
#         "PASSWORD": env.str("DB_PWD"),
#         "HOST": env.str("DB_HOST"),
#         "PORT": env.str("DB_PORT"),
#     }
# }

# If you want to use sqlite3 instead, then uncomment this and comment the above.

# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",
#    }
# }

STATIC_ROOT = str(BASE_DIR / "staticfiles")
STATICFILES_DIRS = (str(BASE_DIR / "static"),)

STATICSTORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Connect to our database remotely
import dj_database_url

DATABASE_URL = env.str("DATABASE_URL")

DATABASES = {
    "default": dj_database_url.config(default=DATABASE_URL),
}
