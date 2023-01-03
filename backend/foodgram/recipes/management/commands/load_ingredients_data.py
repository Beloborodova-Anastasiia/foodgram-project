from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient


def check_not_empty_base(class_type):
    alredy_loaded_error_message = """
        If you need to reload the child data from the CSV file,
        first delete the db file to destroy the database.
        Then, run `python manage.py migrate` for a new empty
        database with tables"""

    if class_type.objects.exists():
        print(f'data in {class_type} already loaded...exiting.')
        print(alredy_loaded_error_message)
        return False
    print(f'Loading data {class_type}')
    return True


class Command(BaseCommand):
    PATH_TO_DATA = '/*/foodgram-project-react/data/ingredients.csv'
    help = "Loads data from .csv files"

    def handle(self, *args, **options):
        if check_not_empty_base(Ingredient):
            for row in DictReader(
                open(self.PATH_TO_DATA),
                fieldnames=['name', 'measurement_unit']
            ):
                ingredient = Ingredient(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )
                ingredient.save()
