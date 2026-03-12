from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


GENRE_CHOICES = [
    ('accion', 'Acción'),
    ('aventura', 'Aventura'),
    ('rpg', 'RPG'),
    ('estrategia', 'Estrategia'),
    ('deportes', 'Deportes'),
    ('carreras', 'Carreras'),
    ('terror', 'Terror / Survival'),
    ('plataformas', 'Plataformas'),
    ('shooter', 'Shooter'),
    ('simulacion', 'Simulación'),
    ('puzzle', 'Puzzle'),
    ('lucha', 'Lucha'),
    ('indie', 'Indie'),
    ('otro', 'Otro'),
]

PLATFORM_CHOICES = [
    ('pc', 'PC'),
    ('ps5', 'PlayStation 5'),
    ('ps4', 'PlayStation 4'),
    ('xbox_series', 'Xbox Series X/S'),
    ('xbox_one', 'Xbox One'),
    ('switch', 'Nintendo Switch'),
    ('mobile', 'Móvil'),
    ('retro', 'Retro / Otra'),
]

STATUS_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('jugando', 'Jugando'),
    ('completado', 'Completado'),
    ('abandonado', 'Abandonado'),
    ('platinado', 'Platinado / 100%'),
]

RATING_CHOICES = [
    (1, '★ Pésimo'),
    (2, '★★ Malo'),
    (3, '★★★ Regular'),
    (4, '★★★★ Bueno'),
    (5, '★★★★★ Obra maestra'),
]


class Game(models.Model):
    """Modelo principal: Videojuego del catálogo personal."""

    # Campo de texto corto (requerido)
    title = models.CharField(max_length=200, verbose_name='Título')

    # Campo de texto corto adicional
    developer = models.CharField(max_length=150, verbose_name='Desarrollador / Estudio')

    # Campo de texto largo (requerido)
    review = models.TextField(
        verbose_name='Reseña personal',
        help_text='Escribe tu opinión, experiencia o descripción del juego.'
    )

    year = models.PositiveIntegerField(verbose_name='Año de lanzamiento')
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES, default='otro', verbose_name='Género')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='pc', verbose_name='Plataforma')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente', verbose_name='Estado')
    rating = models.IntegerField(choices=RATING_CHOICES, default=3, verbose_name='Puntuación')
    hours_played = models.PositiveIntegerField(default=0, verbose_name='Horas jugadas')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name='Portada')
    is_favorite = models.BooleanField(default=False, verbose_name='Favorito')

    # Fecha automática de creación (requerida)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última modificación')

    # ForeignKey con User (requerido)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='games', verbose_name='Propietario')

    class Meta:
        verbose_name = 'Videojuego'
        verbose_name_plural = 'Videojuegos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.year})'

    def get_absolute_url(self):
        return reverse('catalog:game_detail', kwargs={'pk': self.pk})

    def get_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

    def get_status_icon(self):
        icons = {
            'pendiente': '🕐', 'jugando': '🎮',
            'completado': '✅', 'abandonado': '❌', 'platinado': '🏆',
        }
        return icons.get(self.status, '🎮')

    def get_platform_icon(self):
        icons = {
            'pc': '🖥️', 'ps5': '🎮', 'ps4': '🎮',
            'xbox_series': '🎮', 'xbox_one': '🎮',
            'switch': '🕹️', 'mobile': '📱', 'retro': '👾',
        }
        return icons.get(self.platform, '🎮')
