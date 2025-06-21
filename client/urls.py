from django.urls import path
from .views import (
    ClientListView, ClientCreateView,
    ClientUpdateView, ClientDeleteView
)

app_name = "client"

urlpatterns = [
    path("list/",   ClientListView.as_view(),   name="client_list"),
    path("create/", ClientCreateView.as_view(), name="client_create"),
    path("<int:pk>/edit/",   ClientUpdateView.as_view(), name="client_edit"),
    path("<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
]
