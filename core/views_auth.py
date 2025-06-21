# core/views_auth.py
"""
Vistas de autenticación y registro.
"""

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import CustomAuthenticationForm, CustomUserCreationForm


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        auth_login(self.request, self.object)  # login automático
        return response
