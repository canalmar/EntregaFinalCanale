# client/apps.py
from django.apps import AppConfig


class ClientConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "client"

    def ready(self):
        # Importa aquí para que las señales se enganchen al arrancar Django
        import client.signals  # noqa
