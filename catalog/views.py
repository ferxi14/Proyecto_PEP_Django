from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect, get_object_or_404
from .models import Game, Comment
from .forms import GameForm, CustomUserCreationForm, CommentForm


class GameListView(ListView):
    """Vista principal: catálogo completo de videojuegos."""
    model = Game
    template_name = 'catalog/game_list.html'
    context_object_name = 'games'
    paginate_by = 12

    def get_queryset(self):
        queryset = Game.objects.select_related('author').all()
        genre = self.request.GET.get('genre')
        platform = self.request.GET.get('platform')
        search = self.request.GET.get('q')
        if genre:
            queryset = queryset.filter(genre=genre)
        if platform:
            queryset = queryset.filter(platform=platform)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import GENRE_CHOICES, PLATFORM_CHOICES
        context['genre_choices'] = GENRE_CHOICES
        context['platform_choices'] = PLATFORM_CHOICES
        context['selected_genre'] = self.request.GET.get('genre', '')
        context['selected_platform'] = self.request.GET.get('platform', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class MyGamesView(LoginRequiredMixin, ListView):
    """Vista: videojuegos del usuario autenticado."""
    model = Game
    template_name = 'catalog/my_games.html'
    context_object_name = 'games'

    def get_queryset(self):
        return Game.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        games = self.get_queryset()
        context['total'] = games.count()
        context['completados'] = games.filter(status='completado').count()
        context['jugando'] = games.filter(status='jugando').count()
        context['pendientes'] = games.filter(status='pendiente').count()
        context['platinados'] = games.filter(status='platinado').count()
        context['total_horas'] = sum(g.hours_played for g in games)
        return context


class GameDetailView(DetailView):
    """Vista de detalle expandido de un videojuego."""
    model = Game
    template_name = 'catalog/game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pasa la lista de comentarios al template
        context['comments'] = self.object.comments.select_related('author').all()
        # pasa el formulario vacío al template
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Procesa el envío del formulario de comentarios."""
        if not request.user.is_authenticated:
            messages.error(request, 'Debes iniciar sesión para dejar un comentario.')
            return redirect('login')

        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)  # no guarda aún
            comment.game   = self.object       # asigna el juego
            comment.author = request.user      # asigna el usuario
            comment.save()                     # ahora sí guarda
            messages.success(request, '¡Comentario publicado!')
            return redirect('catalog:game_detail', pk=self.object.pk)

        # si hay errores, vuelve a mostrar la página con el formulario con errores
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class GameCreateView(LoginRequiredMixin, CreateView):
    """Vista de creación de un nuevo videojuego."""
    model = Game
    form_class = GameForm
    template_name = 'catalog/game_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'¡Videojuego "{form.instance.title}" añadido a tu catálogo!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Añadir'
        return context


class GameUpdateView(LoginRequiredMixin, UpdateView):
    """Vista de edición de un videojuego existente."""
    model = Game
    form_class = GameForm
    template_name = 'catalog/game_form.html'

    def dispatch(self, request, *args, **kwargs):
        game = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            if game.author != request.user:
                messages.error(
                    request,
                    'No tienes permiso para editar este juego. Solo puedes editar tus propias entradas.'
                )
                return redirect('catalog:game_detail', pk=game.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, f'¡Videojuego "{form.instance.title}" actualizado con éxito!')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Editar'
        return context


class GameDeleteView(LoginRequiredMixin, DeleteView):
    """Vista de confirmación y borrado de un videojuego."""
    model = Game
    template_name = 'catalog/game_confirm_delete.html'
    success_url = reverse_lazy('catalog:game_list')

    def dispatch(self, request, *args, **kwargs):
        game = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            if game.author != request.user:
                messages.error(
                    request,
                    'No tienes permiso para eliminar este juego. Solo puedes borrar tus propias entradas.'
                )
                return redirect('catalog:game_detail', pk=game.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        title = self.get_object().title
        messages.success(self.request, f'El juego "{title}" ha sido eliminado de tu catálogo.')
        return super().form_valid(form)


class SignUpView(FormView):
    """Vista de registro de nuevos usuarios."""
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('catalog:game_list')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, f'¡Bienvenido/a, {user.username}! Tu cuenta ha sido creada. ¡Empieza a añadir tus juegos!')
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'catalog/comment_confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        comment = self.get_object()
        if not request.user.is_staff and not request.user.is_superuser:
            if comment.author != request.user:
                messages.error(request, 'No puedes eliminar comentarios de otros usuarios.')
                return redirect('catalog:game_detail', pk=comment.game.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Comentario eliminado.')
        return reverse('catalog:game_detail', kwargs={'pk': self.object.game.pk})
