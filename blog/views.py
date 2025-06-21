"""
blog/views.py
──────────────
Class-Based Views (CBV) para la app Blog.

Convenciones del proyecto
─────────────────────────
- Identificadores en inglés (clases, funciones, variables).
- Docstrings y mensajes al usuario en español.
- Principio DRY: se reutilizan mixins y helpers siempre que sea posible.
"""

from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .forms import PostForm
from .models import Post

# ──────────────────────────────────────────────────────────────
# Mensajes reutilizables
# ──────────────────────────────────────────────────────────────
MSG_NO_PERMISSION = "No tienes permiso para realizar esta acción."
MSG_CREATED = "Publicación creada correctamente."
MSG_UPDATED = "Publicación actualizada correctamente."
MSG_DELETED = "Publicación eliminada correctamente."

# ──────────────────────────────────────────────────────────────
# Mixins
# ──────────────────────────────────────────────────────────────
class AuthorOrStaffRequiredMixin(UserPassesTestMixin):
    """
    Permite el acceso si el usuario es staff o autor del objeto.
    Se usa en UpdateView y DeleteView de Post.
    """

    # Helpers --------------------------------------------------
    def _current_user_display_name(self) -> str:
        """
        Devuelve el nombre con el que identificamos al usuario actual:
        - Nombre completo si existe.
        - Username en caso contrario.
        """
        return self.request.user.get_full_name() or self.request.user.username

    # Métodos de UserPassesTestMixin ---------------------------
    def test_func(self) -> bool:
        """True si el usuario es staff o autor del post."""
        obj: Post = self.get_object()  # type: ignore[attr-defined]
        user = self.request.user
        return user.is_staff or obj.author == self._current_user_display_name()

    def handle_no_permission(self):
        """Muestra mensaje de error y delega manejo estándar."""
        messages.error(self.request, MSG_NO_PERMISSION)
        return super().handle_no_permission()


# ──────────────────────────────────────────────────────────────
# Vistas públicas
# ──────────────────────────────────────────────────────────────
class PostListView(ListView):
    """
    Lista pública de posts con búsqueda opcional.

    URL:
        /blog/posts/?search=palabra
    """

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # Ajustable

    # Overrides -----------------------------------------------
    def get_queryset(self) -> "QuerySet[Post]":
        """
        Devuelve un queryset filtrado por término de búsqueda
        y ordenado por fecha de creación descendente.
        """
        query: str = self.request.GET.get("search", "").strip()
        qs: QuerySet[Post] = Post.objects.all()
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
    """Crea un nuevo post (cualquier usuario autenticado)."""

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_url = reverse_lazy("blog:post_list")
    success_message = MSG_CREATED

    # Overrides -----------------------------------------------
    def form_valid(self, form):
        """Asigna el autor antes de guardar y muestra mensaje de éxito."""
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
    success_message = MSG_UPDATED


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
    success_message = MSG_DELETED

