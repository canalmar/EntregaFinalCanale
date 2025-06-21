from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from client.models import Client

#@receiver(post_save, sender=User)
#def create_profile(sender, instance, created, **kwargs):
#    if created:
#        Profile.objects.create(user=instance)


# ── crear Profile cuando se crea el usuario ──────────────────────────────────
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# ── sincronizar Client con cambios en Profile y User ─────────────────────────
@receiver(post_save, sender=Profile)
def sync_client_with_profile(sender, instance, **kwargs):
    """Actualiza o crea el registro Client cada vez que se guarda Profile."""
    user = instance.user

    # crea Client si no existe
    client, _ = Client.objects.get_or_create(user=user)

    # copia datos
    client.first_name = user.first_name
    client.last_name  = user.last_name
    client.email      = user.email
    client.phone      = instance.phone
    client.address    = instance.address
    client.save()
