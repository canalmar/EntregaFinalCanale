"""
product/views.py
────────────────
Class-Based Views (CBV) para la app Product.

Secciones
─────────
1. CRUD interno (solo personal `is_staff`)
2. Catálogo público sin autenticación
3. Detalle de producto

Convenciones
────────────
- Identificadores en inglés; docstrings y mensajes al usuario en español.
- Se reutiliza `StaffRequiredMixin` para restringir acceso interno.
- Todos los listados incluyen búsqueda por título, autor o categoría.
"""

from typing import Any, Dict

from django.db.models import Q, QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Product
from .forms import ProductForm
from core.view_mixins import StaffRequiredMixin  # Mixin de permisos

# ─────────────────────────────────────────
# Mensajes reutilizables
# ─────────────────────────────────────────
MSG_CREATED = "Producto creado correctamente."
MSG_UPDATED = "Producto actualizado correctamente."
MSG_DELETED = "Producto eliminado correctamente."

# ------------------------------------------------------------------
# Helpers (funciones internas)
# ------------------------------------------------------------------
def _filter_products(qs: "QuerySet[Product]", query: str) -> "QuerySet[Product]":
    """Aplica filtro por título, autor o categoría (case-insensitive)."""
    if query:
        qs = qs.filter(
            Q(title__icontains=query)
            | Q(author__icontains=query)
            | Q(category__name__icontains=query)
        )
    return qs

# ─────────────────────────────────────────
# CRUD interno (is_staff)
# ─────────────────────────────────────────
class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """
    Lista interna de productos (solo staff), con búsqueda opcional.

    URL:
        /product/list/?search=<cadena>
    """

    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    ordering = ["title"]

    # Overrides -----------------------------------------------
    def get_queryset(self) -> "QuerySet[Product]":
        query: str = self.request.GET.get("search", "").strip()
        qs: QuerySet[Product] = super().get_queryset()
        return _filter_products(qs, query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ProductCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Crea un nuevo producto (solo staff)."""

    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("product:product_list")
    success_message = MSG_CREATED


class ProductUpdateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Actualiza un producto (solo staff)."""

    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("product:product_list")
    success_message = MSG_UPDATED


class ProductDeleteView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Elimina un producto (solo staff)."""

    model = Product
    template_name = "product/product_confirm_delete.html"
    success_url = reverse_lazy("product:product_list")
    success_message = MSG_DELETED


# ─────────────────────────────────────────
# Catálogo público (sin login)
# ─────────────────────────────────────────
class CatalogListView(ListView):
    """
    Catálogo público de productos con buscador.

    URL:
        /product/catalogo/?search=<cadena>
    """

    model = Product
    template_name = "product/product_catalog.html"
    context_object_name = "products"
    ordering = ["title"]

    # Overrides -----------------------------------------------
    def get_queryset(self) -> "QuerySet[Product]":
        query: str = self.request.GET.get("search", "").strip()
        qs: QuerySet[Product] = super().get_queryset()
        return _filter_products(qs, query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ProductDetailView(DetailView):
    """
    Detalle público de un producto.

    Características:
        • No requiere autenticación.
        • Si el usuario es staff, la plantilla puede mostrar botones de
          edición/eliminación (según lógica en el template).
    """

    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"
