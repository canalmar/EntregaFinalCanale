from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """  Formulario para crear y editar productos.
    Utiliza ModelForm para vincularse directamente al modelo Product.
    Aplica clases de Bootstrap para una mejor visualización en el navegador."""

    class Meta:
        model = Product
        fields = '__all__'  # Incluye todos los campos del modelo Product
        widgets = {         #Widgets para personalizar la apariencia de los campos
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
