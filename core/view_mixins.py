"""
core/view_mixins.py
───────────────────
Mixins de autorización reutilizables en todo el proyecto.

Convenciones
────────────
- Solo contienen lógica de permisos (no vistas completas).
- Identificadores en inglés; docstrings y mensajes al usuario en español.
"""

from typing import Any

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

__all__ = ["StaffRequiredMixin"]  # Export explícito


# ──────────────────────────────────────────────────────────────
# Mixins de permisos
# ──────────────────────────────────────────────────────────────
class StaffRequiredMixin(UserPassesTestMixin):
    """
    Restringe el acceso a usuarios con `is_staff=True`.

    Ejemplo de uso:
        class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
            model = Product
            template_name = "product/product_list.html"
    """

    # ----------------------------------------------------------
    # Métodos de UserPassesTestMixin
    # ----------------------------------------------------------
    def test_func(self) -> bool:  # type: ignore[override]
        """Retorna `True` si el usuario es miembro del staff."""
        return self.request.user.is_staff

    def handle_no_permission(self):
        """
        Maneja la redirección cuando el usuario no cumple la condición.

        - Redirige a la ruta “home” sin mostrar mensaje.
        """
        return HttpResponseRedirect(reverse_lazy("core:home"))
