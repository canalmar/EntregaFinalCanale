"""
Django settings for TiendaHistorias project.
Actualizado para desarrollo local y entrega.
Compatible con Django 5.2.x
"""

from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _

# ─────────────────────────────────────────────────────────
#  Rutas base
# ─────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────
#  Seguridad / Debug
# ─────────────────────────────────────────────────────────
SECRET_KEY = "django-insecure-$tgn#%s0ho91u@#w(3ioqk60p&l42c+qltn)td_z^$p_@ngind"

DEBUG = True                       # ← cámbialo a False en producción
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# ─────────────────────────────────────────────────────────
#  Apps instaladas
# ─────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # filtros útiles de formato
    # Apps propias
    "core",
    #"client",
    "client.apps.ClientConfig",
    "product",
    "blog",
]

# ─────────────────────────────────────────────────────────
#  Middleware
# ─────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # ← justo después de SessionMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─────────────────────────────────────────────────────────
#  URLs y WSGI
# ─────────────────────────────────────────────────────────
ROOT_URLCONF = "TiendaHistorias.urls"
WSGI_APPLICATION = "TiendaHistorias.wsgi.application"

# ─────────────────────────────────────────────────────────
#  Templates
# ─────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
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


# ─────────────────────────────────────────────────────────
#  Base de datos (SQLite para curso)
# ─────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ─────────────────────────────────────────────────────────
#  Validadores de contraseña
# ─────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
        "OPTIONS": {"user_attributes": ("username", "email"), "max_similarity": 0.7},
    },
    {
        "NAME": "core.validators.SpanishMinimumLengthValidator",  # ← usamos el nuevo
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────
#  Internacionalización
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE = "es"                       # Español genérico
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True                              # USE_L10N fue retirado en Django 4.0+

# ─────────────────────────────────────────────────────────
#  Archivos estáticos y media
# ─────────────────────────────────────────────────────────
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"     # para collectstatic en producción

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

FIXTURE_DIRS = [BASE_DIR / "fixtures"]

# ─────────────────────────────────────────────────────────
#  Autenticación
# ─────────────────────────────────────────────────────────
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# ─────────────────────────────────────────────────────────
#  Campo ID automático
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

