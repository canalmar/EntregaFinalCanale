from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Client

class ClientModelTest(TestCase):
    def setUp(self):
        self.client_obj = Client.objects.create(
            first_name="Alicia",
            last_name="Lopez",
            email="alicia@example.com",
            phone="123-456-789",
            address="Calle 25 nro 120, Mercedes"
        )

    def test_client_str(self):
        self.assertIn(self.client_obj.first_name, str(self.client_obj))
        self.assertIn(self.client_obj.last_name, str(self.client_obj))

    def test_client_email(self):
        self.assertEqual(self.client_obj.email, "alicia@example.com")

class ClientViewTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        self.client.login(username="staff", password="pass")
        self.client_obj = Client.objects.create(
            first_name="Alicia",
            last_name="Lopez",
            email="alicia@example.com",
            phone="123-456-789",
            address="Calle 25 nro 120, Mercedes"
        )

    def test_client_list_view_status(self):
        url = reverse('client:client_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alicia")

    def test_client_create_permission(self):
        self.client.logout()
        url = reverse('client:client_create')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)  # Solo staff puede acceder
        self.client.login(username="staff", password="pass")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
