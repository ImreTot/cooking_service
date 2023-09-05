import csv
from recipes.models import Ingredient

def add_ingredient_objects_in_database(path):
    with open(path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            name, measurement_unit = row
            ingredient = Ingredient(name=name, measurement_unit=measurement_unit)
            ingredient.save()
