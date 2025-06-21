from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Client
from .forms import ClientForm
from core.view_mixins import StaffRequiredMixin  # mismo mixin usado en product


# ─────────────────────────────────────────
# CRUD (solo empleados is_staff)
# ─────────────────────────────────────────
class ClientListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Listado de clientes con búsqueda por nombre o apellido."""
    model = Client
    template_name = "client/client_list.html"
    context_object_name = "clients"
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        query = self.request.GET.get("search", "").strip()
        qs = super().get_queryset()
        if query:
            qs = qs.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query)
            )
        return qs.order_by("last_name", "first_name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ClientCreateView(LoginRequiredMixin, StaffRequiredMixin,
                       SuccessMessageMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("client:client_list")
    success_message = "Cliente creado correctamente."


class ClientUpdateView(LoginRequiredMixin, StaffRequiredMixin,
                       SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "client/client_form.html"
    success_url = reverse_lazy("client:client_list")
    success_message = "Cliente actualizado correctamente."


class ClientDeleteView(LoginRequiredMixin, StaffRequiredMixin,
                       SuccessMessageMixin, DeleteView):
    model = Client
    template_name = "client/client_confirm_delete.html"
    success_url = reverse_lazy("client:client_list")
    success_message = "Cliente eliminado correctamente."
