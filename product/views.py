"""
product/views.py
────────────────
Class-Based Views (CBV) para la app **Product**.

Secciones
─────────
1. CRUD interno (solo personal `is_staff`)
2. Catálogo público sin autenticación
3. Detalle de producto

Convenciones
────────────
- Identificadores en inglés; docstrings y textos de interfaz en español.
- Se reutiliza `StaffRequiredMixin` para restringir acceso interno.
- Todos los listados incluyen búsqueda por título, autor o categoría.
"""

from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)

from .models import Product
from .forms import ProductForm
from core.view_mixins import StaffRequiredMixin

# ─────────────────────────────────────────
# Mensajes reutilizables
# ─────────────────────────────────────────
MSG_CREATED = "Producto creado correctamente."
MSG_UPDATED = "Producto actualizado correctamente."
MSG_DELETED = "Producto eliminado correctamente."

# ------------------------------------------------------------------
# Helpers
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
# 1. CRUD interno (solo staff)
# ─────────────────────────────────────────
class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    """Listado interno con buscador (solo staff)."""

    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    ordering = ["title"]

    def get_queryset(self) -> "QuerySet[Product]":  # type: ignore[override]
        query = self.request.GET.get("search", "").strip()
        base_qs = super().get_queryset().select_related("category")
        return _filter_products(base_qs, query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # type: ignore[override]
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ProductCreateView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    SuccessMessageMixin,
    CreateView,
):
    """Crear producto (solo staff)."""

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
    """Editar producto (solo staff)."""

    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("product:product_list")
    success_message = MSG_UPDATED


class ProductDeleteView(
    LoginRequiredMixin,
    StaffRequiredMixin,
    DeleteView,
):
    """Eliminar producto (solo staff)."""

    model = Product
    template_name = "product/product_confirm_delete.html"
    success_url = reverse_lazy("product:product_list")
    success_message = MSG_DELETED  # mantener coherencia con el resto

    # SuccessMessageMixin no funciona con DeleteView → mensaje manual
    def delete(
        self, request, *args: Any, **kwargs: Any
    ) -> HttpResponseRedirect:  # type: ignore[override]
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response


# ─────────────────────────────────────────
# 2. Catálogo público
# ─────────────────────────────────────────
class CatalogListView(ListView):
    """Catálogo público con buscador."""

    model = Product
    template_name = "product/product_catalog.html"
    context_object_name = "products"
    ordering = ["title"]

    def get_queryset(self) -> "QuerySet[Product]":  # type: ignore[override]
        query = self.request.GET.get("search", "").strip()
        base_qs = super().get_queryset().select_related("category")
        return _filter_products(base_qs, query)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:  # type: ignore[override]
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


# ─────────────────────────────────────────
# 3. Detalle público
# ─────────────────────────────────────────
class ProductDetailView(DetailView):
    """Detalle público de producto."""

    model = Product
    template_name = "product/product_detail.html"
    context_object_name = "product"
