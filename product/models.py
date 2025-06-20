from django.db import models

class Category(models.Model):
    """  Representa una categoría del catálogo (ej: Aventura, Romance, Misterio, Infantil, etc.).
    Las categorías pueden ser creadas desde el panel de administración o por formulario."""

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    """ Representa un producto del catálogo de Tienda de Historias.
    Puede ser un libro, juego u otro artículo disponible para la venta. """
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

