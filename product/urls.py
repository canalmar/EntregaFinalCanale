from django.urls import path
from . import views

app_name = 'product'  

urlpatterns = [
    path('create/', views.product_create, name='product_create'),
    path('list/', views.product_list, name='product_list'),
    path('edit/<int:product_id>/', views.product_edit, name='product_edit'),
    path('delete/<int:product_id>/', views.product_delete, name='product_delete'),
    path('catalogo/', views.catalog_view, name='product_catalog'),

]