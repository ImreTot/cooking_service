# Generated by Django 4.2.4 on 2023-09-05 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_alter_recipe_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-publication_date']},
        ),
    ]
