# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from client.models import Client


class CustomUserCreationForm(UserCreationForm):
    """Formulario de registro con todos los datos necesarios."""

    first_name = forms.CharField(
        label=_("Nombre"),
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Juan")}
        ),
    )
    last_name = forms.CharField(
        label=_("Apellido"),
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Pérez")}
        ),
    )
    email = forms.EmailField(
        required=True,
        label=_("Correo electrónico"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("tucorreo@ejemplo.com")}
        ),
    )
    address = forms.CharField(
        label=_("Dirección"),
        max_length=255,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("Calle 123")}
        ),
    )
    phone = forms.CharField(
        label=_("Teléfono"),
        max_length=20,
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": _("3515551234")}
        ),
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

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Ese correo ya está registrado."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        Client.objects.update_or_create(
            email=user.email,
            defaults={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "address": self.cleaned_data["address"],
                "phone": self.cleaned_data["phone"],
            },
        )
        return user



class CustomAuthenticationForm(AuthenticationForm):
    """Login con campos Bootstrap."""

    username = forms.CharField(
        label=_("Usuario"),
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Nombre de usuario"),
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Contraseña"),
                "autocomplete": "current-password",
            }
        ),
    )