"""
TiendaHistorias/urls.py
───────────────────────
Enruta las URL principales del proyecto:

• Admin                → /admin/
• Core (home, auth)    → /
• Productos            → /productos/
• Clientes             → /clientes/
• Blog                 → /blog/
• Perfil por defecto   → /accounts/profile/  (redirige al perfil custom)
• Archivos estáticos   → solo en DEBUG (media + static)

Notas
─────
- Mantenemos `django.contrib.auth.urls` para aprovechar vistas predeterminadas
  (password_reset, logout, etc.).
- En producción (`DEBUG = False`) delegá la entrega de archivos estáticos
  al servidor (Nginx, Apache) o un CDN.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.views import profile_redirect

urlpatterns = [
    # Panel de administración
    path("admin/", admin.site.urls),

    # Apps locales
    path("", include("core.urls")),              # Home + auth custom
    path("productos/", include("product.urls")),
    path("clientes/", include("client.urls")),
    path("blog/", include("blog.urls")),

    # Auth por defecto de Django (password_reset, etc.)
    path("accounts/", include("django.contrib.auth.urls")),

    # Redirección del perfil por defecto → perfil custom
    path("accounts/profile/", profile_redirect, name="profile_redirect"),
]

# ----------------------------------------------------------------------
# Servir archivos estáticos y subidos solo en desarrollo
# ----------------------------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0],
    )
