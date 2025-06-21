from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserEditForm, ProfileEditForm
from .models import Profile


class HomeView(TemplateView):
    template_name = "core/index.html"


# core/views.py  ── reemplaza solo esta clase
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Muestra y permite editar:
    • first_name, last_name, email  (User)
    • phone, address                (Profile)
    Si el usuario no tiene Profile, lo crea al vuelo.
    """
    template_name = "core/profile.html"
    success_url   = reverse_lazy("core:profile")
    form_class    = UserEditForm  # se sobreescribe en get_context_data

    def get_object(self, queryset=None):
        return self.request.user

    # ───────────────────────────────────────
    # helper para garantizar que exista el perfil
    def _get_or_create_profile(self):
        from .models import Profile
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile
    # ───────────────────────────────────────

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self._get_or_create_profile()

        if self.request.method == "POST":
            context["user_form"]    = UserEditForm(self.request.POST, instance=self.request.user)
            context["profile_form"] = ProfileEditForm(self.request.POST, instance=profile)
        else:
            context["user_form"]    = UserEditForm(instance=self.request.user)
            context["profile_form"] = ProfileEditForm(instance=profile)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        profile = self._get_or_create_profile()

        user_form    = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(self.success_url)

        return self.render_to_response(
            self.get_context_data(
                user_form=user_form,
                profile_form=profile_form,
            )
        )


@login_required
def profile_redirect(request):
    """Redirige /accounts/profile/ al perfil custom."""
    return redirect("core:profile")


class AboutView(TemplateView):
    template_name = "core/about.html"
