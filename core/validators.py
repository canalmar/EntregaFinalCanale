"""
core/validators.py
──────────────────
Validadores personalizados para el proyecto.

Incluye:
- SpanishMinimumLengthValidator: replica `MinimumLengthValidator` de Django,
  pero con mensajes completamente en español.

Cómo usarlo
───────────
Añade la clase a `AUTH_PASSWORD_VALIDATORS` en `settings.py`, por ejemplo:

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "core.validators.SpanishMinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
]
"""

from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

__all__ = ["SpanishMinimumLengthValidator"]


class SpanishMinimumLengthValidator(MinimumLengthValidator):
    """
    Validador de longitud mínima de contraseña con mensajes en español.

    Parámetros (opciones en settings):
        • min_length (int): Longitud mínima permitida (por defecto 8).

    Ejemplo:
        {"NAME": "core.validators.SpanishMinimumLengthValidator",
         "OPTIONS": {"min_length": 10}}
    """

    # ----------------------------------------------------------
    # Overrides de MinimumLengthValidator
    # ----------------------------------------------------------
    def get_help_text(self) -> str:  # noqa: D401
        """Texto de ayuda mostrado en formularios de registro/login."""
        return _(
            "La contraseña debe contener al menos %(min_length)d caracteres."
        ) % {"min_length": self.min_length}

    def validate(self, password: str, user=None) -> None:
        """
        Lanza ValidationError si la contraseña no cumple la longitud mínima.
        """
        if len(password) < self.min_length:
            raise ValidationError(
                _(
                    "Esta contraseña es demasiado corta. "
                    "Debe contener al menos %(min_length)d caracteres."
                ),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
