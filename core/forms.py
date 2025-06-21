# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from client.models import Client
from .models import Profile


# ────────────────────────────────────────────────────────────────────────────
# REGISTRO
# ────────────────────────────────────────────────────────────────────────────
class CustomUserCreationForm(UserCreationForm):
    """Registro extendido: nombre, apellido, email, teléfono y dirección."""

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
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": _("3515551234")}),
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

    # ---- Estilo Bootstrap para todos los campos ---------------------------
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
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

    # ---- Validación de email único ----------------------------------------
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Ese correo ya está registrado."))
        return email

    # ---- Guardado: User, Profile y Client ---------------------------------
    def save(self, commit: bool = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()

        # 1. PERFIL (teléfono y dirección)
        profile, _ = Profile.objects.get_or_create(user=user)
        profile.phone   = self.cleaned_data.get("phone", "")
        profile.address = self.cleaned_data.get("address", "")
        profile.save()

        # 2. CLIENT (registro visible para empleados)
        client, created = Client.objects.get_or_create(user=user)
        client.first_name = user.first_name
        client.last_name  = user.last_name
        client.email      = user.email
        client.phone      = profile.phone
        client.address    = profile.address
        client.save()

        return user


# ────────────────────────────────────────────────────────────────────────────
# LOGIN
# ────────────────────────────────────────────────────────────────────────────
class CustomAuthenticationForm(AuthenticationForm):
    """Login con campos Bootstrap."""

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


# ────────────────────────────────────────────────────────────────────────────
# EDICIÓN PERFIL
# ────────────────────────────────────────────────────────────────────────────
class UserEditForm(forms.ModelForm):
    """Edita nombre, apellido y email."""

    first_name = forms.CharField(label="Nombre",  required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name  = forms.CharField(label="Apellido", required=False,
                                 widget=forms.TextInput(attrs={"class": "form-control"}))
    email      = forms.EmailField(label="Correo", required=False,
                                  widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model  = User
        fields = ("first_name", "last_name", "email")


class ProfileEditForm(forms.ModelForm):
    """Edita teléfono y dirección."""

    phone   = forms.CharField(label="Teléfono",  required=False,
                              widget=forms.TextInput(attrs={"class": "form-control"}))
    address = forms.CharField(label="Dirección", required=False,
                              widget=forms.TextInput(attrs={"class": "form-control"}))

    class Meta:
        model  = Profile
        fields = ("phone", "address")
