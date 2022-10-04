from csv import DictReader

from django.core.management import BaseCommand

from recipes.models import Ingredient


FILE_PATH = 'F:/Programming/Code/foodgram-project-react/data/ingredients.csv'


class Command(BaseCommand):
    help = 'Load data from .csv file'

    def handle(self, *args, **kwds):
        print('Loading data from .csv file')
        fieldnames = ['name', 'measurement_unit']
        for row in DictReader(
            open(FILE_PATH, encoding="utf-8"), fieldnames=fieldnames
        ):
            ingredient = Ingredient(name=row['name'],
                                    measurement_unit=row['measurement_unit'])
            ingredient.save()
        print('ingredients.csv uploaded')
