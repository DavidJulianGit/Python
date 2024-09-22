from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


DEFAULT_APP = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
CREATED_APP = ["apps.recipes", "apps.auth"]

THIRD_PARTY_APP = [
    "markdownx",
    "markdownify",
]  # third party apps go here

INSTALLED_APPS = [*DEFAULT_APP, *CREATED_APP, *THIRD_PARTY_APP]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "recipe_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "apps" / "core" / "templates"),
            str(BASE_DIR / "apps" / "recipes" / "templates"),
            str(BASE_DIR / "apps" / "auth" / "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "recipe_project.wsgi.application"


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

STATIC_URL = "/static/"
STATICFILES_DIRS = [str(BASE_DIR / "static")]


MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
MARKDOWNIFY = {
    "default": {
        "WHITELIST_TAGS": [
            "h1",
            "h2",
            "h3",
            "h4",
            "a",
            "p",
            "strong",
            "em",
            "ol",
            "ul",
            "li",
            "code",
            "pre",
            "blockquote",
            "img",
        ],
        "WHITELIST_ATTRS": {"*": ["class"], "a": ["href", "target"], "img": ["src"]},
        "MARKDOWN_EXTENSIONS": [
            "markdown.extensions.extra",  # Includes list support
            "markdown.extensions.codehilite",
        ],
        "STRIP": False,
    }
}

LOGIN_URL = "/login/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
