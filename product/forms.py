from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Formulario para crear y editar productos.
    Se vincula al modelo Product y usa clases Bootstrap.
    """

    class Meta:
        model = Product
        fields = "__all__"          # Usa todos los campos del modelo
        widgets = {
            "name":        forms.TextInput(attrs={"class": "form-control"}),
            "author":      forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "price":       forms.NumberInput(attrs={"class": "form-control"}),
            "category":    forms.Select(attrs={"class": "form-select"}),
            "image":       forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
