# core/urls.py
from django.urls import path
from .views import HomeView          
from .views_auth import UserLoginView, UserLogoutView, UserRegisterView

app_name = "core"          

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/",    UserLoginView.as_view(),  name="login"),
    path("accounts/login/", UserLoginView.as_view()),
    path("logout/",   UserLogoutView.as_view(), name="logout"),
    path("register/", UserRegisterView.as_view(), name="register"),
 
]
