from django.test import TestCase
from django.urls import reverse
from .models import Profile
from django.contrib.auth import get_user_model

class ProfileModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = self.user.profile  # Usar el perfil creado automáticamente por la señal

    def test_profile_str(self):
        self.assertIn(self.user.username, str(self.profile))

    def test_profile_user(self):
        self.assertEqual(self.profile.user.username, "testuser")

class HomeViewTest(TestCase):
    def test_home_view_status(self):
        url = reverse('core:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Tienda de Historias', response.content)

class AboutViewTest(TestCase):
    def test_about_view_status(self):
        url = reverse('core:about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Acerca de', response.content)
