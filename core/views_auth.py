"""
core/views_auth.py
──────────────────
Vistas dedicadas a la autenticación y registro de usuarios.

Incluye:
- UserLoginView    → Inicio de sesión.
- UserLogoutView   → Cierre de sesión.
- UserRegisterView → Registro con alta automática en sesión.
"""

from typing import Any

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import CustomAuthenticationForm, CustomUserCreationForm

# ──────────────────────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────────────────────
class UserLoginView(LoginView):
    """
    Vista de inicio de sesión.

    Características:
        • Usa `CustomAuthenticationForm` con estilo Bootstrap.
        • Si el usuario ya está autenticado, lo redirige a `next_page`
          (por defecto, la HOME definida en settings o `core:home`).
    """

    template_name = "registration/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


# ──────────────────────────────────────────────────────────────
# LOGOUT
# ──────────────────────────────────────────────────────────────
class UserLogoutView(LogoutView):
    """
    Cierra la sesión y redirige a la portada.

    La URL de destino se define con `next_page`.
    """
    next_page = reverse_lazy("core:home")


# ──────────────────────────────────────────────────────────────
# REGISTRO
# ──────────────────────────────────────────────────────────────
class UserRegisterView(CreateView):
    """
    Vista de registro extendido.

    • Usa `CustomUserCreationForm`, que guarda `User`, `Profile` y `Client`.
    • Inicia sesión automáticamente tras el alta.
    """

    form_class = CustomUserCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("core:home")

    # ------------------------------------------------------------------
    # Overrides
    # ------------------------------------------------------------------
    def form_valid(self, form: CustomUserCreationForm) -> HttpResponseRedirect:  # type: ignore[override]
        """
        Si el formulario es válido:

        1. Crea al usuario (y entidades relacionadas).
        2. Inicia sesión automáticamente (`auth_login`).
        3. Redirige a `success_url`.
        """
        response = super().form_valid(form)
        auth_login(self.request, self.object)
        return response
