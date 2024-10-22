# import_showrooms.py
import csv
from django.core.management.base import BaseCommand
from cars.models import ShowRoom

class Command(BaseCommand):
    help = 'Load data from CSV file into the ShowRoom model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file to load')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                showroom_name = row['showroom_name']
                showroom_location = row['showroom_location']
                showroom_regency = row['showroom_regency']

                # Create a new ShowRoom object
                ShowRoom.objects.create(
                    showroom_name=showroom_name,
                    showroom_location=showroom_location,
                    showroom_regency=showroom_regency
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file}'))

