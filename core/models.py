"""
core/models.py
──────────────
Modelos complementarios al sistema de autenticación.

Incluye:
- Profile: datos de contacto adicionales para cada `User`.
"""

from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Datos adicionales asociados a un usuario.

    Campos:
        user (OneToOneField): Enlace 1-a-1 con `auth.User`.
        phone (CharField)   : Teléfono de contacto (opcional).
        address (CharField) : Dirección postal (opcional).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Usuario propietario del perfil.",
    )
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)

    class Meta:
        ordering = ["user__username"]
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    # ------------------------------------------------------------------
    # Métodos utilitarios
    # ------------------------------------------------------------------
    def __str__(self) -> str:  # noqa: D401
        """Devuelve una representación legible para el admin."""
        return f"Perfil de {self.user.username}"

    @property
    def user_full_name(self) -> str:
        """Nombre completo del usuario (útil en plantillas)."""
        return self.user.get_full_name() or self.user.username

