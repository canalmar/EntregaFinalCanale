"""
Modelos de la aplicación Blog.

Incluye:
- Category: Representa las categorías de las publicaciones.
- Post: Representa cada entrada del blog, con título, contenido, imagen, categoría y fecha de creación.
"""

from django.db import models


class Category(models.Model):
    """
    Modelo que representa una categoría para clasificar publicaciones del blog.
  """
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Devuelve el nombre de la categoría como representación del objeto."""
        return self.name


class Post(models.Model):
    """
    Modelo que representa una publicación del blog.

    Campos:
        title (CharField): Título de la publicación.
        author (CharField): Autor (puede quedar en blanco).
        content (TextField): Contenido principal del post.
        image (ImageField): Imagen opcional relacionada con el post.
        category (ForeignKey): Relación con una categoría (puede ser nula).
        created (DateTimeField): Fecha y hora de creación (se asigna automáticamente).
    """
    title   = models.CharField(max_length=120)
    author = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    image   = models.ImageField(upload_to="blog", blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        """Devuelve el título del post como representación del objeto."""
        return self.title

