"""
blog/forms.py
─────────────
Formularios para la creación y edición de publicaciones en la app Blog.
"""

from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """
    Formulario Bootstrap para crear o editar publicaciones del blog.

    Campos editables:
        • title     – Título (requerido).
        • author    – Autor (opcional, se completa auto en vistas protegidas).
        • content   – Contenido principal.
        • image     – Imagen opcional (solo JPG o PNG).
        • category  – Categoría a la que pertenece el post.
    """

    class Meta:
        model = Post
        fields = ["title", "author", "content", "image", "category"]
        labels = {
            "title": "Título",
            "author": "Autor",
            "content": "Contenido",
            "image": "Imagen (opcional)",
            "category": "Categoría",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "author": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={"class": "form-control", "rows": 6}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    # ------------------------------------------------------------------
    # Validaciones y normalizaciones
    # ------------------------------------------------------------------
    def clean_title(self) -> str:
        """
        Normaliza el título:
        - Elimina espacios extra al inicio/fin.
        - Convierte duplicados de espacios internos a uno solo.
        """
        title = self.cleaned_data["title"].strip()
        return " ".join(title.split())

    def clean_author(self) -> str:
        """
        Normaliza el nombre de autor a 'Title Case' sin espacios múltiples.
        (Se ejecuta solo si el campo viene desde el formulario; las vistas
        protegidas lo sobreescribirán con el usuario autenticado).
        """
        author = self.cleaned_data.get("author", "").strip()
        return " ".join(author.title().split())

    def clean_image(self):
        """
        Acepta únicamente imágenes JPEG o PNG.
        Si no se envía imagen, devuelve None (válido).
        """
        image = self.cleaned_data.get("image")
        if image and image.content_type not in ("image/jpeg", "image/png"):
            raise forms.ValidationError(
                "Solo se permiten imágenes JPEG o PNG."
            )
        return image
