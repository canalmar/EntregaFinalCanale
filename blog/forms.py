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
            "title":    forms.TextInput(attrs={"class": "form-control"}),
            "author":   forms.TextInput(attrs={"class": "form-control"}),
            "content":  forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image":    forms.ClearableFileInput(attrs={"class": "form-control"}),
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
        title: str = self.cleaned_data["title"].strip()
        return " ".join(title.split())

    def clean_author(self) -> str:
        """
        Normaliza el nombre de autor a 'Title Case' sin espacios múltiples.
        (Se ejecuta solo si el campo viene desde el formulario; las vistas
        protegidas lo sobreescribirán con el usuario autenticado).
        """
        author: str = self.cleaned_data.get("author", "").strip()
        return " ".join(author.title().split())

    def clean_image(self):
        """
        Valida la imagen solo si el usuario sube una nueva.

        • Permite dejar la imagen existente (cuando se edita un post sin cambiar la foto).
        • Acepta JPG, PNG y WEBP de hasta 2 MB.
        """
        image = self.cleaned_data.get("image")

        # 1) Sin archivo nuevo → mantener la imagen actual
        if not image or hasattr(image, "url"):  # ImageFieldFile ya guardado
            return image

        # 2) Validación de tipo MIME y tamaño
        valid_types = {"image/jpeg", "image/png", "image/webp"}
        if image.content_type not in valid_types:
            raise forms.ValidationError(
                "Formato de imagen no permitido. Solo JPG, PNG o WEBP."
            )

        if image.size > 2 * 1024 * 1024:  # 2 MB
            raise forms.ValidationError("La imagen no puede superar los 2 MB.")

        return image
