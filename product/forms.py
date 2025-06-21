"""
product/forms.py
────────────────
Formularios para la gestión de productos (libros) en la Tienda de
Historias.

Incluye:
- ProductForm: alta y edición con integración Bootstrap.
"""

from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    """
    Formulario Bootstrap para crear o editar productos.

    Campos derivados del modelo `Product`:
        • name         – Título de la obra.
        • author       – Autor.
        • description  – Descripción corta.
        • price        – Precio en pesos argentinos.
        • category     – Categoría literaria.
        • image        – Imagen de portada (opcional).
    """

    class Meta:
        model = Product
        fields = "__all__"  # Usa todos los campos definidos en Product
        labels = {
            "name": "Título",
            "author": "Autor",
            "description": "Descripción",
            "price": "Precio",
            "category": "Categoría",
            "image": "Imagen (opcional)",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": 0, "step": "0.01"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    # ------------------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------------------
    def clean_name(self) -> str:
        """
        Normaliza el título:
        - Quita espacios sobrantes.
        - Convierte duplicados de espacios internos a uno solo.
        """
        name = self.cleaned_data["name"].strip()
        return " ".join(name.split())

    def clean_price(self) -> float:
        """
        Verifica que el precio sea positivo.
        """
        price = self.cleaned_data["price"]
        if price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price
