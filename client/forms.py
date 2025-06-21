"""
client/forms.py
───────────────
Formularios para la gestión de clientes en la Tienda de Historias.

Objetivo
────────
Proveer una interfaz Bootstrap limpia (class="form-control") para crear
y editar fichas de clientes (`ClientForm`).
"""

from django import forms

from .models import Client


class ClientForm(forms.ModelForm):
    """
    Formulario Bootstrap para crear o editar fichas de clientes.

    Campos visibles:
        • first_name  – Nombre
        • last_name   – Apellido
        • email       – E-mail
        • phone       – Teléfono
        • address     – Dirección

    Notas:
        • Los widgets usan `form-control` para integrarse con el layout Bootstrap 5
          aplicado en las plantillas.
        • La validación de tipos y longitudes la gestiona automáticamente Django
          según los campos definidos en `Client`.
    """

    class Meta:
        model = Client
        fields = ["first_name", "last_name", "email", "phone", "address"]
        labels = {
            "first_name": "Nombre",
            "last_name":  "Apellido",
            "email":      "E-mail",
            "phone":      "Teléfono",
            "address":    "Dirección",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name":  forms.TextInput(attrs={"class": "form-control"}),
            "email":      forms.EmailInput(attrs={"class": "form-control"}),
            # Usamos type="tel" para facilitar teclado numérico en móviles
            "phone":      forms.TextInput(attrs={"class": "form-control", "type": "tel"}),
            "address":    forms.TextInput(attrs={"class": "form-control"}),
        }

    # ------------------------------------------------------------------
    # Validaciones personalizadas
    # ------------------------------------------------------------------
    def clean_email(self):
        """
        Normaliza el e-mail a minúsculas para evitar falsos duplicados en
        validaciones case-insensitive.
        """
        return self.cleaned_data["email"].lower()
