# Generated by Django 4.2.4 on 2023-09-10 11:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'ordering': ['-user']},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['-name']},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ['-recipe']},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'ordering': ['-user']},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['-follower']},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-slug']},
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1, message='Too short a period of time.'), django.core.validators.MaxValueValidator(limit_value=32000, message='Too long a period of time.')]),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=32000, message='Amount value is too high.'), django.core.validators.MinValueValidator(limit_value=1, message='Amount value is too small')]),
        ),
    ]