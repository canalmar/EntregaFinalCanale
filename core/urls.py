from django.urls import path
from .views import HomeView, ProfileUpdateView, AboutView
from .views_auth import UserLoginView, UserLogoutView, UserRegisterView

app_name = "core"

urlpatterns = [
    # Home
    path("", HomeView.as_view(), name="home"),

    # Autenticación
    path("login/",    UserLoginView.as_view(),  name="login"),
    path("accounts/login/", UserLoginView.as_view()),   # alias
    path("logout/",   UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),

    # Perfil (CBV que permite ver/editar)
    path("perfil/", ProfileUpdateView.as_view(), name="profile"),

    # About
    path("about/", AboutView.as_view(), name="about"),
]

    # Vista FBV protegida 
    #path("perfil/", profile, name="profile"),

