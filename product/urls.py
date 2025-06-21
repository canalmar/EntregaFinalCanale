from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductUpdateView,
    ProductDeleteView, CatalogListView
)

app_name = "product"

urlpatterns = [
    # Catálogo público
    path("catalogo/", CatalogListView.as_view(), name="catalog_view"),

    # CRUD staff
    path("list/",   ProductListView.as_view(),   name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<int:pk>/edit/",   ProductUpdateView.as_view(), name="product_edit"),
    path("<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
]
