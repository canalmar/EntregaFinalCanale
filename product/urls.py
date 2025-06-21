"""
product/urls.py
───────────────
Rutas para la app Product, encargada de gestionar el catálogo
interno y la visualización pública de productos.

Secciones
─────────
• Catálogo público (`catalog_view`)
• CRUD para personal autorizado (`product_*`)
• Detalle de producto sin autenticación (`product_detail`)

Notas
─────
- El listado “interno” (`ProductListView`) está pensado para usuarios staff
  y se diferencia del “catálogo” público (`CatalogListView`).
"""

from django.urls import path

from .views import (
    CatalogListView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView,
)

app_name = "product"

urlpatterns = [
    # Catálogo público
    path("catalogo/", CatalogListView.as_view(), name="catalog_view"),

    # CRUD interno (requiere autenticación y permisos staff)
    path("list/", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/edit/", ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),

    # Detalle público (accesible sin login)
    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
