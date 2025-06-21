"""
client/views.py
───────────────
Class-Based Views (CBV) para la gestión de clientes en la Tienda de Historias.

Convenciones
────────────
- Identificadores en inglés (clases, funciones, variables).
- Docstrings y mensajes mostrados al usuario en español.
- Acceso restringido a personal (`is_staff`) mediante `StaffRequiredMixin`.
- Principio DRY: reutilizamos mixins y evitamos lógica duplicada.
"""

from typing import Any, Dict

from django.db.models import Q, QuerySet
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Client
from .forms import ClientForm
from core.view_mixins import StaffRequiredMixin  # Reutilizado también en 'product' app

# ─────────────────────────────────────────
# Mensajes reutilizables
# ─────────────────────────────────────────
MSG_CREATED = "Cliente creado correctamente."
MSG_UPDATED = "Cliente actualizado correctamente."
MSG_DELETED = "Cliente eliminado correctamente."

# ─────────────────────────────────────────
# CRUD (solo empleados `is_staff`)
# ─────────────────────────────────────────
class ClientListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """
    Lista de clientes con búsqueda opcional por nombre o apellido.

    URL:
        /client/list/?search=<cadena>
    """

    model = Client
    template_name = "client/client_list.html"
    context_object_name = "clients"
    ordering = ["last_name", "first_name"]

    # Overrides -----------------------------------------------
    def get_queryset(self) -> "QuerySet[Client]":
        """Filtra por término de búsqueda y omite registros sin nombre/apellido."""
        query: str = self.request.GET.get("search", "").strip()

        qs: QuerySet[Client] = super().get_queryset().exclude(
            first_name__exact="", last_name__exact=""
        )
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return qs.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Mantiene el valor de búsqueda en el contexto para la plantilla."""
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ClientCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Crea una nueva ficha de cliente (solo personal autorizado)."""

    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("client:client_list")
    success_message = MSG_CREATED


class ClientUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Actualiza una ficha de cliente existente (solo personal autorizado)."""

    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("client:client_list")
    success_message = MSG_UPDATED


class ClientDeleteView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Elimina una ficha de cliente existente (solo personal autorizado)."""

    model = Client
    template_name = "client/client_confirm_delete.html"
    success_url = reverse_lazy("client:client_list")
    success_message = MSG_DELETED
