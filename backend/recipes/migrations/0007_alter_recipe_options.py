# Generated by Django 4.2.4 on 2023-09-05 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredient_measurement_unit_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['publication_date']},
        ),
    ]
