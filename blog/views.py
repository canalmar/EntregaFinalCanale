"""
blog/views.py
──────────────
Vistas basadas en clases (CBV) para el módulo Blog.

Convenciones del proyecto
─────────────────────────
- Nombres de clases, funciones y variables en inglés (profesional).
- Docstrings y mensajes al usuario en español.
- Principio DRY: reutilizamos mixins y evitamos repetir lógica.
"""

from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin

from .models import Post
from .forms import PostForm


# ──────────────────────────────────────────────────────────────
# Mixins
# ──────────────────────────────────────────────────────────────
class AuthorOrStaffRequiredMixin(UserPassesTestMixin):
    """
    Permite el acceso si el usuario es staff o es autor del objeto.
    Se usa para UpdateView y DeleteView de Post.
    """

    def test_func(self) -> bool:
        """Verifica si el usuario actual es staff o autor del post."""
        obj: Post = self.get_object()  # type: ignore[attr-defined]
        user = self.request.user
        return user.is_staff or obj.author == (user.get_full_name() or user.username)

    def handle_no_permission(self):
        """Muestra mensaje de error y redirige si no tiene permiso."""
        messages.error(
            self.request,
            "No tienes permiso para realizar esta acción.",
        )
        return super().handle_no_permission()


# ──────────────────────────────────────────────────────────────
# Vistas públicas
# ──────────────────────────────────────────────────────────────
class PostListView(ListView):
    """
    Lista pública de posts con búsqueda opcional.
    URL esperada: /blog/posts/?search=palabra
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # Ajustable

    def get_queryset(self):
        """Filtra por término de búsqueda y ordena por fecha desc."""
        query: str = self.request.GET.get("search", "").strip()
        qs = Post.objects.all()
        if query:
            qs = qs.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(category__name__icontains=query)
            )
        return qs.order_by("-created")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        """Agrega 'search' al contexto para mantener el valor en la plantilla."""
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "").strip()
        return context


class PostDetailView(DetailView):
    """Vista pública de detalle de un post."""
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


# ──────────────────────────────────────────────────────────────
# CRUD (requieren autenticación)
# ──────────────────────────────────────────────────────────────
class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Crea un nuevo post.
    - Cualquier usuario autenticado.
    """
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "Publicación creada correctamente."

    def form_valid(self, form):
        """Asigna el autor antes de guardar."""
        post: Post = form.save(commit=False)  # type: ignore[assignment]
        post.author = self.request.user.get_full_name() or self.request.user.username
        post.save()
        return super().form_valid(form)


class PostUpdateView(
    LoginRequiredMixin,
    AuthorOrStaffRequiredMixin,
    SuccessMessageMixin,
    UpdateView,
):
    """Actualiza un post existente (autor o staff)."""
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "Publicación actualizada correctamente."


class PostDeleteView(
    LoginRequiredMixin,
    AuthorOrStaffRequiredMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """Elimina un post existente (autor o staff)."""
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = "Publicación eliminada correctamente."
