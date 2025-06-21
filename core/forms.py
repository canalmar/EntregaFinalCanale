"""
core/forms.py
─────────────
Formularios de autenticación, registro y edición de perfil
para la Tienda de Historias.

Convenciones
────────────
- Identificadores en inglés; docstrings y textos al usuario en español.
- Bootstrap 5 (`class="form-control"`) aplicado a todos los inputs.
- Se sincronizan los modelos auxiliares `Profile` y `Client` cuando
  el usuario se registra o edita sus datos.
"""

from typing import Any, Dict

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from client.models import Client
from .models import Profile

# ──────────────────────────────────────────────────────────────
# REGISTRO
# ──────────────────────────────────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    """
    Formulario de registro extendido.

    Campos extra:
        • first_name – Nombre
        • last_name  – Apellido
        • email      – Correo (único)
        • address    – Dirección (opcional)
        • phone      – Teléfono (opcional)
    """

    first_name = forms.CharField(
        label=_("Nombre"),
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Juan")}),
    )
    last_name = forms.CharField(
        label=_("Apellido"),
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Pérez")}),
    )
    email = forms.EmailField(
        label=_("Correo electrónico"),
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": _("tucorreo@ejemplo.com")}),
    )
    address = forms.CharField(
        label=_("Dirección"),
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("Calle 123")}),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("3515551234"), "type": "tel"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "address",
            "phone",
            "password1",
            "password2",
        )
        labels = {"username": _("Usuario")}

    # ----------------------------------------------------------
    # Init: placeholders + Bootstrap
    # ----------------------------------------------------------
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        placeholders: Dict[str, str] = {
            "username": _("Elige un nombre de usuario"),
            "first_name": _("Juan"),
            "last_name": _("Pérez"),
            "email": _("tucorreo@ejemplo.com"),
            "address": _("Calle 123"),
            "phone": _("3515551234"),
            "password1": _("Contraseña"),
            "password2": _("Confirma tu contraseña"),
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs["placeholder"] = placeholders.get(name, "")
        self.fields["password1"].help_text = ""

    # ----------------------------------------------------------
    # Validaciones
    # ----------------------------------------------------------
    def clean_email(self) -> str:
        """Valida unicidad de e-mail (case-insensitive)."""
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Ese correo ya está registrado."))
        return email

    def clean_first_name(self) -> str:
        """Normaliza nombre (sin espacios extra, Title Case)."""
        return " ".join(self.cleaned_data["first_name"].strip().title().split())

    def clean_last_name(self) -> str:
        """Normaliza apellido (sin espacios extra, Title Case)."""
        return " ".join(self.cleaned_data["last_name"].strip().title().split())

    # ----------------------------------------------------------
    # Guardado: User + Profile + Client
    # ----------------------------------------------------------
    def save(self, commit: bool = True) -> User:  # type: ignore[override]
        """Crea el usuario y sincroniza Profile + Client."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()

        # 1. Profile (teléfono y dirección)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.phone = self.cleaned_data.get("phone", "")
        profile.address = self.cleaned_data.get("address", "")
        profile.save()

        # 2. Client (registro visible para empleados)
        client, _ = Client.objects.get_or_create(user=user)
        client.first_name = user.first_name
        client.last_name = user.last_name
        client.email = user.email
        client.phone = profile.phone
        client.address = profile.address
        client.save()

        return user


# ──────────────────────────────────────────────────────────────
# LOGIN
# ──────────────────────────────────────────────────────────────
class CustomAuthenticationForm(AuthenticationForm):
    """Formulario de inicio de sesión con estilo Bootstrap."""

    username = forms.CharField(
        label=_("Usuario"),
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Nombre de usuario"), "autofocus": True}
        ),
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": _("Contraseña"), "autocomplete": "current-password"}
        ),
    )


# ──────────────────────────────────────────────────────────────
# EDICIÓN DE PERFIL
# ──────────────────────────────────────────────────────────────
class UserEditForm(forms.ModelForm):
    """Editar nombre, apellido y e-mail del usuario."""

    first_name = forms.CharField(
        label=_("Nombre"),
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        label=_("Apellido"),
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label=_("Correo"),
        required=False,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    """Editar teléfono y dirección del perfil."""

    phone = forms.CharField(
        label=_("Teléfono"),
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "type": "tel"}),
    )
    address = forms.CharField(
        label=_("Dirección"),
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Profile
        fields = ("phone", "address")

