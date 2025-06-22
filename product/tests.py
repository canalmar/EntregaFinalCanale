from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Infantil")
        self.product = Product.objects.create(
            title="El árbol generoso",
            author="Shel Silverstein",
            description="Cuento ilustrado.",
            price=29.90,
            stock=10,
            category=self.category
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "El árbol generoso")

    def test_product_fields(self):
        self.assertEqual(self.product.author, "Shel Silverstein")
        self.assertEqual(self.product.stock, 10)

class ProductViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Infantil")
        self.product = Product.objects.create(
            title="El árbol generoso",
            author="Shel Silverstein",
            description="Cuento ilustrado.",
            price=29.90,
            stock=10,
            category=self.category
        )
        User = get_user_model()
        self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        self.client.login(username="staff", password="pass")

    def test_product_list_view_status(self):
        url = reverse('product:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "El árbol generoso")

    def test_product_create_permission(self):
        self.client.logout()
        url = reverse('product:product_create')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)  # Solo staff puede acceder
        self.client.login(username="staff", password="pass")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
