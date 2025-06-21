"""
client/models.py
────────────────
Modelo Client: ficha de datos de contacto de clientes para la Tienda de Historias.

Puntos clave
────────────
- Relación 1-a-1 con `django.contrib.auth.models.User` para mantener
  sincronizados los datos de autenticación y la ficha comercial.
- Todos los campos son opcionales salvo `created_at`; así evitamos errores si
  se crea la ficha antes de que el usuario complete su perfil.
"""

from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    """
    Modelo que almacena la información de contacto de un cliente.

    Campos:
        user (OneToOneField): Usuario asociado (puede ser nulo hasta que se registre).
        first_name (CharField): Nombre del cliente.
        last_name (CharField): Apellido del cliente.
        email (EmailField): Correo electrónico.
        phone (CharField): Teléfono de contacto.
        address (CharField): Dirección postal.
        created_at (DateTimeField): Fecha de alta (se asigna automáticamente).
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_record",
        null=True,
        blank=True,
        help_text="Usuario vinculado; permite login y sincroniza datos básicos.",
    )
    first_name = models.CharField("Nombre", max_length=50, blank=True)
    last_name = models.CharField("Apellido", max_length=50, blank=True)
    email = models.EmailField("Correo", blank=True)
    phone = models.CharField("Teléfono", max_length=30, blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)
    created_at = models.DateTimeField("Fecha de alta", auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    # ------------------------------------------------------------------
    # Métodos utilitarios
    # ------------------------------------------------------------------
    def __str__(self) -> str:
        """Devuelve un nombre legible para el administrador."""
        full_name = f"{self.last_name}, {self.first_name}".strip(", ")
        return full_name or f"Client #{self.pk}"

    @property
    def full_name(self) -> str:
        """Nombre completo útil en plantillas y reportes."""
        return f"{self.first_name} {self.last_name}".strip()

