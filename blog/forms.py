from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    Formulario para crear o editar un post.
    Incluye título, contenido, imagen opcional y categoría.
    """
    class Meta:
        model = Post
        fields = ["title", "content", "image", "category"]
        labels = {  
            "title": "Título",
            "content": "Contenido",
            "image": "Imagen (opcional)",
            "category": "Categoría",
        }
        widgets = {
            "title":    forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "content":  forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image":    forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
