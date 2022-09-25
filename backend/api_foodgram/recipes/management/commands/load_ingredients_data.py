from csv import DictReader

from django.core.management import BaseCommand

from api_foodgram.constants import PATH_TO_DATA
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
            for row in DictReader(
                open(PATH_TO_DATA),
                fieldnames=['name', 'measurement_unit']
            ):
                ingredient = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                ingredient.save()
