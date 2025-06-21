from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """Datos extra para cada usuario."""
    user    = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone   = models.CharField("Teléfono",  max_length=30,  blank=True)
    address = models.CharField("Dirección", max_length=255, blank=True)

    def __str__(self) -> str:
        return f"Perfil de {self.user.username}"
