# Generated by Django 4.2.4 on 2023-08-16 10:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_remove_recipeingredient_unit_ingredient_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='unit',
            new_name='measurement_unit',
        ),
    ]
