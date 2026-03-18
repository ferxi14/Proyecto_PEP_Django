from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Game, Comment


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['title', 'developer', 'year', 'genre', 'platform', 'status', 'rating', 'hours_played', 'review', 'cover', 'is_favorite']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: The Legend of Zelda: Breath of the Wild'}),
            'developer': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Nintendo'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 2017', 'min': 1950, 'max': 2099}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control','min': '0','max': '10','step': '0.25','placeholder': 'Ej: 8.75',}),
            'hours_played': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0', 'min': 0}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Escribe tu reseña personal, qué te ha parecido, puntos fuertes y débiles...'}),
            'cover': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_favorite': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Título del juego',
            'developer': 'Desarrollador / Estudio',
            'year': 'Año de lanzamiento',
            'genre': 'Género',
            'platform': 'Plataforma',
            'status': 'Estado',
            'rating': 'Puntuación (0 - 10)',
            'hours_played': 'Horas jugadas',
            'review': 'Reseña personal',
            'cover': 'Portada (imagen)',
            'is_favorite': 'Marcar como favorito',
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
        label='Correo electrónico'
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirmar contraseña'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Escribe tu comentario sobre este juego...',
                'maxlength': 1000,
            })
        }
        labels = {
            'body': ''   # sin etiqueta, la ponemos en el template
        }
