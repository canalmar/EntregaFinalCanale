from django.db.models import Q
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Product
from .forms import ProductForm
from core.view_mixins import StaffRequiredMixin  # ← el mixin que acabamos de crear


# ─────────────────────────────────────────
# CRUD para empleados (is_staff)
# ─────────────────────────────────────────
class ProductListView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Product
    template_name = "product/product_list.html"
    context_object_name = "products"
    ordering = ["title"]

    def get_queryset(self):
        query = self.request.GET.get("search", "").strip()
        qs = super().get_queryset()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__name__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx


class ProductCreateView(LoginRequiredMixin, StaffRequiredMixin,
                        SuccessMessageMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("product:product_list")
    success_message = "Producto creado correctamente."


class ProductUpdateView(LoginRequiredMixin, StaffRequiredMixin,
                        SuccessMessageMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product/product_form.html"
    success_url = reverse_lazy("product:product_list")
    success_message = "Producto actualizado correctamente."


class ProductDeleteView(LoginRequiredMixin, StaffRequiredMixin,
                        SuccessMessageMixin, DeleteView):
    model = Product
    template_name = "product/product_confirm_delete.html"
    success_url = reverse_lazy("product:product_list")
    success_message = "Producto eliminado correctamente."


# ─────────────────────────────────────────
# Catálogo público (sin login)
# ─────────────────────────────────────────
class CatalogListView(ListView):
    model = Product
    template_name = "product/product_catalog.html"
    context_object_name = "products"
    ordering = ["title"]

    def get_queryset(self):
        query = self.request.GET.get("search", "").strip()
        qs = super().get_queryset()
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__name__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search"] = self.request.GET.get("search", "").strip()
        return ctx
