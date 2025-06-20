from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import ProductForm
from .models import Product


# ───────────────────────────────────────────────────────────────────────────────
# Helpers
# ───────────────────────────────────────────────────────────────────────────────
def is_staff(user):
    """Retorna True si el usuario está autenticado y es empleado (is_staff)."""
    return user.is_authenticated and user.is_staff


# ───────────────────────────────────────────────────────────────────────────────
# CRUD para empleados
# ───────────────────────────────────────────────────────────────────────────────
@user_passes_test(is_staff)
def product_create(request):
    """
    Crea un nuevo producto.
    GET  → muestra formulario vacío.
    POST → valida, guarda y redirige al listado con mensaje de éxito.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado correctamente.")
            return redirect("product:product_list")
    else:
        form = ProductForm()

    return render(request, "product/product_form.html", {"form": form})


@user_passes_test(is_staff)
def product_list(request):
    """
    Lista de productos para empleados con filtro opcional (?search=).
    Filtra por título, autor o nombre de categoría (ForeignKey).
    """
    query = request.GET.get("search", "").strip()

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        ).order_by("title")
    else:
        products = Product.objects.all().order_by("title")

    context = {"products": products, "search": query}
    return render(request, "product/product_list.html", context)


@user_passes_test(is_staff)
def product_edit(request, product_id):
    """
    Edita un producto existente.
    GET  → muestra formulario con datos actuales.  
    POST → guarda cambios y redirige con mensaje de éxito.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect("product:product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "product/product_form.html", {"form": form})


@user_passes_test(is_staff)
def product_delete(request, product_id):
    """
    Elimina un producto tras confirmación.
    GET  → muestra plantilla de confirmación.  
    POST → borra y redirige con mensaje de éxito.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Producto eliminado correctamente.")
        return redirect("product:product_list")

    return render(request, "product/product_confirm_delete.html", {"product": product})


# ───────────────────────────────────────────────────────────────────────────────
# Catálogo público
# ───────────────────────────────────────────────────────────────────────────────
def catalog_view(request):
    """
    Muestra el catálogo público en formato tarjetas con búsqueda opcional.
    Se filtra por título, autor o nombre de categoría.  
    """
    query = request.GET.get("search", "").strip()

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(category__name__icontains=query)
        ).order_by("title")
    else:
        products = Product.objects.all().order_by("title")

    context = {"products": products, "search": query}
    return render(request, "product/product_catalog.html", context)







