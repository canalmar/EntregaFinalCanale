"""
TiendaHistorias/settings.py
───────────────────────────
Configuración principal del proyecto **Tienda de Historias**.

Pensado para entorno de desarrollo local y entrega académica
(compatible con Django 5.2.x).

Guías rápidas
─────────────
• En producción, mover las variables sensibles (SECRET_KEY, DEBUG, DB, e-mails)
  a variables de entorno mediante `os.getenv` o un gestor de secretos.
• Para internacionalizar, usá `LANGUAGE_CODE = "es-ar"` si querés el locale
  específico de Argentina.
"""

from pathlib import Path
import os  # noqa: F401 – puede usarse si migrás a variables de entorno
from django.utils.translation import gettext_lazy as _

# ─────────────────────────────────────────────────────────
#  Rutas base
# ─────────────────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────
#  Seguridad / Debug
# ─────────────────────────────────────────────────────────
# ¡Nunca subas tu SECRET_KEY real a un repo público!
SECRET_KEY: str = (
    "django-insecure-$tgn#%s0ho91u@#w(3ioqk60p&l42c+qltn)td_z^$p_@ngind"
    # Para producción: os.getenv("DJANGO_SECRET_KEY")
)

DEBUG: bool = True  # ← cambiá a False en producción

ALLOWED_HOSTS: list[str] = ["127.0.0.1", "localhost"]
# Ej.: ["mi-dominio.com", "www.mi-dominio.com"]

# ─────────────────────────────────────────────────────────
#  Apps instaladas
# ─────────────────────────────────────────────────────────
INSTALLED_APPS: list[str] = [
    # Core Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Filtros útiles de formato

    # Local apps
    "core",
    "client.apps.ClientConfig",  # Modo explícito (reemplaza el string simple)
    "product",
    "blog",
]

# ─────────────────────────────────────────────────────────
#  Middleware
# ─────────────────────────────────────────────────────────
MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # ← después de Session
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ─────────────────────────────────────────────────────────
#  URLs y WSGI
# ─────────────────────────────────────────────────────────
ROOT_URLCONF: str = "TiendaHistorias.urls"
WSGI_APPLICATION: str = "TiendaHistorias.wsgi.application"

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
#  Base de datos
# ─────────────────────────────────────────────────────────
# Para curso usamos SQLite. Cambiá a PostgreSQL en producción.
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
        "OPTIONS": {
            "user_attributes": ("username", "email"),
            "max_similarity": 0.7,
        },
    },
    {
        "NAME": "core.validators.SpanishMinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────
#  Internacionalización
# ─────────────────────────────────────────────────────────
LANGUAGE_CODE: str = "es"  # Español genérico
TIME_ZONE: str = "America/Argentina/Buenos_Aires"
USE_I18N: bool = True
USE_TZ: bool = True  # USE_L10N fue retirado en Django 4.0+

# ─────────────────────────────────────────────────────────
#  Archivos estáticos y de usuario
# ─────────────────────────────────────────────────────────
STATIC_URL: str = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT: Path = BASE_DIR / "staticfiles"

MEDIA_URL: str = "/media/"
MEDIA_ROOT: Path = BASE_DIR / "media"

FIXTURE_DIRS = [BASE_DIR / "fixtures"]

# ─────────────────────────────────────────────────────────
#  Config. de autenticación
# ─────────────────────────────────────────────────────────
LOGIN_URL = "core:login"
LOGIN_REDIRECT_URL = "core:home"
LOGOUT_REDIRECT_URL = "core:home"
SESSION_EXPIRE_AT_BROWSER_CLOSE: bool = True

# ─────────────────────────────────────────────────────────
#  Campo ID automático
# ─────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
