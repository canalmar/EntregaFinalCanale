from django.test import TestCase
from django.urls import reverse
from .models import Post, Category

class BlogModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Novedades")
        self.post = Post.objects.create(
            title="Novedades de Julio",
            author="Tienda de Historias",
            content="<p>Durante julio envio gratis en compras mayores a 15000.</p>",
            category=self.category
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), "Novedades de Julio")

    def test_post_category(self):
        self.assertEqual(self.post.category.name, "Novedades")

class BlogViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Novedades")
        self.post = Post.objects.create(
            title="Novedades de Julio",
            author="Tienda de Historias",
            content="<p>Durante julio envio gratis en compras mayores a 15000.</p>",
            category=self.category
        )

    def test_post_list_view_status(self):
        url = reverse('blog:post_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Novedades de Julio")

    def test_post_detail_view_status(self):
        url = reverse('blog:post_detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Novedades de Julio")
