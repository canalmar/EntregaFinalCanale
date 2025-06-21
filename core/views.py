# core/views.py
from django.views.generic import TemplateView
from django.shortcuts import render, redirect


class HomeView(TemplateView):
    """
    Vista de inicio (home) simple.
    Renderiza el template 'core/index.html'.
    """
    template_name = "core/index.html"  


def profile_redirect(request):
    """Captura /accounts/profile/ y envía al Home."""
    return redirect("core:home")