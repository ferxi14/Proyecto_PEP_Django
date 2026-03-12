from django.contrib import admin
from .models import Game

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'developer', 'year', 'genre', 'platform', 'status', 'rating', 'hours_played', 'author', 'created_at']
    list_filter = ['genre', 'platform', 'status', 'rating', 'is_favorite']
    search_fields = ['title', 'developer', 'review', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Información principal', {'fields': ('title', 'developer', 'year', 'genre', 'platform', 'cover')}),
        ('Estado y valoración', {'fields': ('status', 'rating', 'hours_played', 'is_favorite')}),
        ('Contenido', {'fields': ('review',)}),
        ('Metadatos', {'fields': ('author', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
