from django.db import migrations, models

# Función que convierte las notas antiguas (1-5) al nuevo rango (2-10)
def convertir_ratings(apps, schema_editor):
    Game = apps.get_model('catalog', 'Game')
    for game in Game.objects.all():
        game.rating = float(game.rating) * 2  # 3 → 6.0, 5 → 10.0
        game.save()

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_game_rating_comment'),
    ]

    operations = [
        # Primero convierte los datos ANTES de cambiar el tipo de campo
        migrations.RunPython(convertir_ratings, migrations.RunPython.noop),
        # Luego cambia el campo
        migrations.AlterField(
            model_name='game',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=4, verbose_name='Puntuación'),
        ),
    ]
