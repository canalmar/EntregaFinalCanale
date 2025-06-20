from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("posts/", views.post_list, name="post_list"),
    path("posts/create/", views.post_create, name="post_create"),
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),       # público
    path("posts/<int:post_id>/edit/", views.post_edit, name="post_edit"),      # staff
    path("posts/<int:post_id>/delete/", views.post_delete, name="post_delete") # staff
]
