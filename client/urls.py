from django.urls import path
from . import views

app_name = 'client'

urlpatterns = [
    path('', views.client_list, name='client_list'),
    path("clients/create/", views.client_create, name="client_create"), 
    path("clients/<int:client_id>/edit/", views.client_edit, name="client_edit"), 
    path("clients/<int:client_id>/delete/", views.client_delete, name="client_delete"),

]
