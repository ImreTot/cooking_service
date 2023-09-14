import csv

from recipes.models import Ingredient


def add_ingredient_objects_in_database(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        ingredient_list = [
            Ingredient(name=name,
                       measurement_unit=measurement_unit)
            for name, measurement_unit in csv_reader
        ]
        Ingredient.objects.bulk_create(ingredient_list)
