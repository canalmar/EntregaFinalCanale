"""
client/urls.py
──────────────
Rutas para la gestión de clientes en la Tienda de Historias.

Incluye (por defecto):
- Listado de clientes (`client_list`)
- Edición de un cliente (`client_edit`)
- Eliminación de un cliente (`client_delete`)

⚠️  La ruta de creación (`client_create`) se mantiene comentada porque,
según el flujo actual, los clientes se generan de forma automática
al registrarse usuarios.  
Si más adelante querés habilitar el alta manual, se puede descomentar la línea
de import y la correspondiente entrada en `urlpatterns`.
"""

from django.urls import path

from .views import (
    ClientListView,
    # ClientCreateView,  # ← Descomentar si se habilita la creación manual
    ClientUpdateView,
    ClientDeleteView,
)

app_name = "client"

urlpatterns = [
    path("list/", ClientListView.as_view(), name="client_list"),
    # path("create/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/edit/", ClientUpdateView.as_view(), name="client_edit"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
