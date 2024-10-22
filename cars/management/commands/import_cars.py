# import_cars.py
import csv
from django.core.management.base import BaseCommand
from cars.models import Car, ShowRoom

class Command(BaseCommand):
    help = 'Load data from CSV file into the Car model'

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

                # Try to get or create a showroom based on name, location, and regency
                showroom, created = ShowRoom.objects.get_or_create(
                    showroom_name=showroom_name,
                    showroom_location=showroom_location,
                    showroom_regency=showroom_regency
                )

                # Create a new Car object
                Car.objects.create(
                    showroom=showroom,  # Set the foreign key to the showroom instance
                    brand=row['id_merk'],
                    car_type=row['type'],
                    model=row['model'],
                    color=row['color'],
                    year=row['year'],
                    transmission=row['id_transmission'],
                    fuel_type=row['id_fuel_type'],
                    doors=row['door'],
                    cylinder_size=row['cylinder_size'],
                    cylinder_total=row['cylinder_total'],
                    turbo=row['turbo'] == 1,  # Convert to boolean
                    mileage=row['mileage'],
                    license_plate=row['license_plate'],
                    price_cash=row['price_cash'],
                    price_credit=row['price_credit'],
                    pkb_value=row['nilai_jual_pkb'],
                    pkb_base=row['pkb_pokok'],
                    stnk_date=row['stnk_date'],
                    levy_date=row['levy_date'],
                    swdkllj=row['swdkllj'],
                    total_levy=row['total_levy'],
                    created_at=row['created_at'],
                    updated_at=row['updated_at'],
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file}'))
