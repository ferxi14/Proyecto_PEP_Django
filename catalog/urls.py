from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Catálogo público
    path('', views.GameListView.as_view(), name='game_list'),
    path('mis-juegos/', views.MyGamesView.as_view(), name='my_games'),

    # CRUD completo
    path('juego/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('juego/nuevo/', views.GameCreateView.as_view(), name='game_create'),
    path('juego/<int:pk>/editar/', views.GameUpdateView.as_view(), name='game_update'),
    path('juego/<int:pk>/eliminar/', views.GameDeleteView.as_view(), name='game_delete'),
    path('comentario/<int:pk>/eliminar/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
