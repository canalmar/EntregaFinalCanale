"""
core/views.py
─────────────
Vistas genéricas de la app Core:

• HomeView            – Portada del sitio.
• ProfileUpdateView   – Edición de datos de usuario y perfil.
• profile_redirect    – Redirección del perfil por defecto de Django.
• AboutView           – Página “Acerca de”.

Convenciones
────────────
- Identificadores en inglés; docstrings y mensajes al usuario en español.
- Se reutilizan formularios (`UserEditForm`, `ProfileEditForm`) y se
  garantiza que cada usuario tenga un `Profile`.
"""

from typing import Any, Dict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from .forms import UserEditForm, ProfileEditForm
from .models import Profile


class HomeView(TemplateView):
    """Portada del sitio."""
    template_name = "core/index.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Permite al usuario editar sus datos básicos y de contacto.

    Edita:
        • first_name, last_name, email  (modelo User)
        • phone, address                (modelo Profile)

    Notas:
        - Si el usuario aún no posee `Profile`, se crea automáticamente.
        - Se manejan dos formularios independientes dentro del mismo template.
    """

    template_name = "core/profile.html"
    success_url = reverse_lazy("core:profile")
    form_class = UserEditForm  # Placeholder; los forms reales se inyectan en `get_context_data`

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _get_or_create_profile(self) -> Profile:
        """Devuelve el Profile del usuario, creándolo si no existe."""
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    # ------------------------------------------------------------------
    # UpdateView overrides
    # ------------------------------------------------------------------
    def get_object(self, queryset=None):
        """El objeto principal es siempre la instancia de User."""
        return self.request.user

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Genera el contexto con ambos formularios:

        - `user_form`    para datos de User
        - `profile_form` para datos de Profile
        """
        context = super().get_context_data(**kwargs)
        profile = self._get_or_create_profile()

        if self.request.method == "POST":
            context["user_form"] = UserEditForm(self.request.POST, instance=self.request.user)
            context["profile_form"] = ProfileEditForm(self.request.POST, instance=profile)
        else:
            context["user_form"] = UserEditForm(instance=self.request.user)
            context["profile_form"] = ProfileEditForm(instance=profile)

        return context

    def post(self, request, *args, **kwargs):
        """Procesa la edición simultánea de User y Profile."""
        self.object = self.get_object()
        profile = self._get_or_create_profile()

        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)

        # Si algún formulario falla, se re-renderiza la página con errores.
        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                profile_form=profile_form,
            )
        )


@login_required
def profile_redirect(request):
    """Redirige `/accounts/profile/` al perfil personalizado del sitio."""
    return redirect("core:profile")


class AboutView(TemplateView):
    """Página estática “Acerca de mí / del proyecto”."""
    template_name = "core/about.html"

