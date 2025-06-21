"""
core/view_mixins.py
───────────────────
Mixins reutilizables en todo el proyecto.

Convenciones
────────────
- Solo lógica de autorización / reutilizable.
- Docstrings en español.
"""

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Permite acceso solo a usuarios *staff* (is_staff=True).

    Uso:
        class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
            ...
    """

    # Lógica principal
    def test_func(self):
        return self.request.user.is_staff

    # Redirección en caso de permisos insuficientes
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta vista.")
        return HttpResponseRedirect(reverse_lazy("core:home"))  # Ajusta la ruta si es necesario
