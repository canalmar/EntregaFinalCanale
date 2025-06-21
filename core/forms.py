# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario de registro:

    • email obligatorio y único (case-insensitive)
    • password1 y password2 heredados y visibles
    • widgets Bootstrap
    """

    email = forms.EmailField(
        required=True,
        label=_("Correo electrónico"),
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": _("tucorreo@ejemplo.com")}
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # ← importante: incluir ambos passwords
        fields = ("username", "email", "password1", "password2")
        labels = {"username": _("Usuario")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "username": _("Elige un nombre de usuario"),
            "email": _("tucorreo@ejemplo.com"),
            "password1": _("Contraseña"),
            "password2": _("Confirma tu contraseña"),
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs["placeholder"] = placeholders.get(name, "")

        # >>> Oculta las reglas hasta que haya errores
        self.fields["password1"].help_text = ""


    # ───── Validación email único ─────
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_("Ese correo ya está registrado."))
        return email

    # ───── Guardado normalizando email ─────
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
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
