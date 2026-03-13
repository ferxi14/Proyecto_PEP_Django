from django.contrib import admin
from .models import Game, Comment

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

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['author', 'game', 'created_at', 'short_body']
    list_filter   = ['created_at']
    search_fields = ['author__username', 'game__title', 'body']
    readonly_fields = ['created_at']

    def short_body(self, obj):
        return obj.body[:60] + '...' if len(obj.body) > 60 else obj.body
    short_body.short_description = 'Comentario'
