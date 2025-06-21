from django.db import models
from django.contrib.auth.models import User

#class Client(models.Model):
#    """ Representa un cliente de Tienda de Historias.
#    Incluye información  de contacto. """
#    
#    first_name = models.CharField(max_length=100)
#    last_name = models.CharField(max_length=100)
#    email = models.EmailField(unique=True)
#    address = models.CharField(max_length=255)
#    phone = models.CharField(max_length=20, blank=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return f"{self.first_name} {self.last_name}"
#

class Client(models.Model):
    """
    Registro que ve el staff. Representa un cliente de Tienda de Historias.
    Incluye información  de contacto.
    Se enlaza 1-a-1 con User para poder sincronizar cambios.
    """
    user       = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="client_record",
        null=True, blank=True,
    )
    first_name = models.CharField("Nombre",    max_length=50, blank=True)
    last_name  = models.CharField("Apellido",  max_length=50, blank=True)
    email      = models.EmailField("Correo",   blank=True)
    phone      = models.CharField("Teléfono",  max_length=30, blank=True)
    address    = models.CharField("Dirección", max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

