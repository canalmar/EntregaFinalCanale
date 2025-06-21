"""
product/models.py
─────────────────
Modelos para el catálogo de la Tienda de Historias.

Incluye:
- Category: clasificación temática (Aventura, Romance, etc.).
- Product : ítems disponibles para la venta (libros, juegos u otros).
"""

from django.db import models


class Category(models.Model):
    """
    Categoría del catálogo (ej.: Aventura, Romance, Misterio).

    Campos:
        name (CharField): Nombre único de la categoría.
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # ------------------------------------------------------------------
    # Métodos utilitarios
    # ------------------------------------------------------------------
    def __str__(self) -> str:  # noqa: D401
        """Devuelve el nombre de la categoría."""
        return self.name


class Product(models.Model):
    """
    Producto del catálogo.

    Puede ser un libro, juego u otro artículo disponible para la venta.

    Campos:
        title (CharField)        : Título de la obra.
        author (CharField)       : Autor o creador.
        description (TextField)  : Descripción corta.
        price (DecimalField)     : Precio (máx. 999 999,99).
        stock (PositiveInteger)  : Unidades disponibles.
        category (ForeignKey)    : Categoría temática (opcional).
        image (ImageField)       : Imagen de portada (opcional).
        created_at (DateTime)    : Fecha de alta (auto).
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Categoría temática del producto (opcional).",
    )
    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # ------------------------------------------------------------------
    # Métodos utilitarios
    # ------------------------------------------------------------------
    def __str__(self) -> str:  # noqa: D401
        """Devuelve el título del producto."""
        return self.title

