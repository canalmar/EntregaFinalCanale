"""
core/urls.py
────────────
Rutas principales de la aplicación Core:

• Home          → Portada.
• Auth          → Login, Logout, Registro.
• Profile       → Vista/edición de perfil.
• About         → Página estática “Acerca de”.

Notas
─────
- Se mantiene un alias a `/accounts/login/` para compatibilidad con
  plantillas o apps que utilicen la URL por defecto de Django.
- La antigua vista basada en función (`profile_redirect`) quedó integrada
  directamente como CBV (`ProfileUpdateView`). Si se necesita restaurar,
  descomentar el import y la entrada correspondiente.
"""

from django.urls import path

from .views import HomeView, ProfileUpdateView, AboutView
from .views_auth import UserLoginView, UserLogoutView, UserRegisterView

app_name = "core"

urlpatterns = [
    # Home
    path("", HomeView.as_view(), name="home"),

    # Autenticación
    path("login/", UserLoginView.as_view(), name="login"),
    path("accounts/login/", UserLoginView.as_view()),  # Alias para compatibilidad
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),

    # Perfil (CBV que permite ver/editar)
    path("perfil/", ProfileUpdateView.as_view(), name="profile"),

    # Página “Acerca de…”
    path("about/", AboutView.as_view(), name="about"),
]

# ------------------------------------------------------------------
# FBV opcional:
# ------------------------------------------------------------------
# from .views import profile_redirect
# path("perfil/", profile_redirect, name="profile"),

