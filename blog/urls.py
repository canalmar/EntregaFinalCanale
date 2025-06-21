"""
Rutas de la aplicación Blog.

Define las URL para listar, ver detalle, crear, editar y eliminar publicaciones.
"""

from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/create/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_edit"),
    path("posts/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post_delete"),
]
