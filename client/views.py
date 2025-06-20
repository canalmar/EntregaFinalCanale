from django.shortcuts import render,  redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from .forms import ClientForm
from django.contrib import messages

from .models import Client


def is_staff(user):
    """True si el usuario está logueado y tiene is_staff=True."""
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff)
def client_list(request):
    """ Lista de clientes con búsqueda opcional (?search=).
    Filtra por nombre o apellido y ordena alfabéticamente por last_name. """
    
    query = request.GET.get("search", "").strip()

    if query:
        clients = Client.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).order_by("last_name", "first_name")
    else:
        clients = Client.objects.all().order_by("last_name", "first_name")

    return render(request,"client/client_list.html",{"clients": clients, "search": query})


@user_passes_test(is_staff)
def client_create(request):
    """ Crea un nuevo cliente.
    GET  → muestra formulario vacío.  
    POST → valida, guarda y redirige con mensaje de éxito. """
    
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente creado correctamente.")
            return redirect("client:client_list")
    else:
        form = ClientForm()

    return render(request, "client/client_form.html", {"form": form})

@user_passes_test(is_staff)
def client_edit(request, client_id):
    """   Edita un cliente existente.
    GET  → muestra formulario con datos actuales.  
    POST → guarda cambios y redirige con mensaje de éxito."""
    
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente actualizado correctamente.")
            return redirect("client:client_list")
    else:
        form = ClientForm(instance=client)

    return render(request, "client/client_form.html", {"form": form})


@user_passes_test(is_staff)
def client_delete(request, client_id):
    """ Elimina un cliente tras confirmación.
    GET  → muestra plantilla de confirmación.  
    POST → borra y redirige con mensaje de éxito. """
    
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        client.delete()
        messages.success(request, "Cliente eliminado correctamente.")
        return redirect("client:client_list")

    return render(request, "client/client_confirm_delete.html", {"client": client})




