# core/validators.py
from django.contrib.auth.password_validation import MinimumLengthValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class SpanishMinimumLengthValidator(MinimumLengthValidator):
    """
    Igual que MinimumLengthValidator pero con mensaje en español.
    """

    def get_help_text(self):
        return _("La contraseña debe contener al menos %(min_length)d caracteres.") % {
            "min_length": self.min_length
        }

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("Esta contraseña es demasiado corta. Debe contener al menos %(min_length)d caracteres."),
                code="password_too_short",
                params={"min_length": self.min_length},
            )
