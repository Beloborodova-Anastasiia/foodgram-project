from csv import DictReader
import readline

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404
from recipes.models import Ingredient

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


def check_not_empty_base(class_type):
    if class_type.objects.exists():
        print(f'data in {class_type} already loaded...exiting.')
        print(ALREDY_LOADED_ERROR_MESSAGE)
        empty_base = False
    else:
        print(f'Loading data {class_type}')
        empty_base = True
    return empty_base


class Command(BaseCommand):
    help = "Loads data from .csv files"

    def handle(self, *args, **options):

        if check_not_empty_base(Ingredient):
            while True:
                try:
                    file = input('Enter path to csv file:\n')
                    ingredients = open(file)
                except FileNotFoundError:
                    print('No such file or directory')
                else:
                    break

            while True:
                data = ingredients.readline()
                if data != '':
                    data = data.replace('\n', '')
                    data_list = data.split(',')
                    ingredient = Ingredient(
                        name=data_list[0],
                        measurement_unit=data_list[1],
                    )
                    ingredient.save()
                else:
                    break

