from django.test import TestCase
from .models import Car, ShowRoom
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import CarEditForm
from .forms import AddCarForm

#Model test untuk model car dan showroom
class ModelTest(TestCase):
    def setUp(self):
        self.showroom = ShowRoom.objects.create(
            showroom_name="Best Cars",
            showroom_location="123 Car St",
            showroom_regency="Regency A"
        )

    def test_create_car(self):
        car = Car.objects.create(
            showroom=self.showroom,
            brand="Toyota",
            car_type="SUV",
            model="Fortuner",
            color="White",
            year=2020,
            transmission="Automatic",
            fuel_type="Diesel",
            doors=5,
            cylinder_size=2400,
            cylinder_total=4,
            turbo=True,
            mileage=20000,
            license_plate="B1234XYZ",
            price_cash=500000000,
            price_credit=520000000,
            pkb_value=3000000,
            pkb_base=2900000,
            stnk_date="2025-10-10",
            levy_date="2025-10-11",
            swdkllj=150000,
            total_levy=320000
        )
        self.assertEqual(car.showroom, self.showroom)
        self.assertEqual(car.brand, "Toyota")

# View test untuk akses  role-based
class ViewTest(TestCase):
    def setUp(self):
        # Membuat user biasa dan admin
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        # Membuat showroom contoh
        self.showroom = ShowRoom.objects.create(
            showroom_name="Test Showroom",
            showroom_location="Main Street",
            showroom_regency="Regency A"
        )

        # Membuat objek mobil 
        self.car = Car.objects.create(
            showroom=self.showroom,
            brand="Toyota",
            car_type="SUV",
            model="Fortuner",
            color="White",
            year=2020,
            transmission="Automatic",
            fuel_type="Diesel",
            doors=5,
            cylinder_size=2400,
            cylinder_total=4,
            turbo=False,
            mileage=30000,
            license_plate="B5678XYZ",
            price_cash=500000000,
            price_credit=520000000,
            pkb_value=3000000,
            pkb_base=2900000,
            stnk_date="2025-12-31",
            levy_date="2025-12-31",
            swdkllj=150000,
            total_levy=320000
        )


    def test_view_car_detail(self):
        url = reverse('car_detail', args=[self.car.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


    def test_edit_car_access_admin_only(self):
        # Login sebagai admin
        self.client.login(username='admin', password='admin123')
        
        # Membuat URL edit car dengan UUID sebagai argumen
        url = reverse('edit_car', args=[str(self.car.id)])  # Konversi UUID ke string untuk URL
        response = self.client.get(url)
        
        # Periksa apakah admin memiliki akses ke halaman edit
        self.assertEqual(response.status_code, 200)

        

class CarEditFormTest(TestCase):
    def test_car_edit_form_valid_data(self):
        form_data = {
            'model': 'Avanza',
            'color': 'White',
            'year': 2020,
            'fuel_type': 'Gasoline',
            'cylinder_size': 1500,
            'mileage': 20000,
            'stnk_date': '2025-12-31',
            'levy_date': '2025-12-31',
            'license_plate': 'B1234XYZ',
            'price_cash': 150000000,
            'price_credit': 160000000,
        }
        form = CarEditForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_car_edit_form_invalid_data(self):
        
        form = CarEditForm(data={})
        self.assertFalse(form.is_valid())
        
        required_fields = ['model', 'color', 'year', 'fuel_type', 'cylinder_size', 'mileage', 
                           'stnk_date', 'levy_date', 'license_plate', 'price_cash', 'price_credit']
        for field in required_fields:
            self.assertIn(field, form.errors)
            
class AddCarFormTest(TestCase):
    def test_add_car_form_valid_data(self):
        form_data = {
            'brand': 'Toyota',
            'car_type': 'SUV',
            'model': 'Fortuner',
            'color': 'Black',
            'year': 2021,
            'transmission': 'Automatic',
            'fuel_type': 'Diesel',
            'doors': 5,
            'cylinder_size': 2400,
            'cylinder_total': 4,
            'turbo': True,
            'mileage': 30000,
            'license_plate': 'B5678ABC',
            'price_cash': 400000000,
            'price_credit': 420000000,
            'pkb_value': 3000000,
            'pkb_base': 2900000,
            'stnk_date': '2025-11-30',
            'levy_date': '2025-11-30',
            'swdkllj': 120000,
            'total_levy': 312000,
            'showroom_name': 'Best Showroom',
            'showroom_location': '123 Showroom St',
            'showroom_regency': 'Regency A',
        }
        form = AddCarForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_add_car_form_missing_required_fields(self):
        form = AddCarForm(data={})
        self.assertFalse(form.is_valid())
        required_fields = ['brand', 'car_type', 'model', 'color', 'year', 'transmission', 'fuel_type',
                           'doors', 'cylinder_size', 'cylinder_total', 'mileage', 'license_plate',
                           'price_cash', 'price_credit', 'pkb_value', 'pkb_base', 'stnk_date', 'levy_date',
                           'swdkllj', 'total_levy', 'showroom_name', 'showroom_location', 'showroom_regency']
        for field in required_fields:
            self.assertIn(field, form.errors)

#Ajax test untuk add dan delete mobil       
class AjaxTest(TestCase):
    def setUp(self):
        # Membuat admin untuk mengakses fitur yang membutuhkan otorisasi admin
        self.admin_user = User.objects.create_superuser(username='admin', password='admin123')

        # Membuat showroom 
        self.showroom = ShowRoom.objects.create(
            showroom_name="Sample Showroom",
            showroom_location="Broadway",
            showroom_regency="Regency B"
        )

        # Membuat objek mobil 
        self.car = Car.objects.create(
            showroom=self.showroom,
            brand="Honda",
            car_type="Sedan",
            model="Accord",
            color="Black",
            year=2021,
            transmission="Manual",
            fuel_type="Petrol",
            doors=4,
            cylinder_size=1800,
            cylinder_total=4,
            turbo=True,
            mileage=15000,
            license_plate="D9876ABC",
            price_cash=400000000,
            price_credit=420000000,
            pkb_value=2800000,
            pkb_base=2700000,
            stnk_date="2025-11-30",
            levy_date="2025-11-30",
            swdkllj=130000,
            total_levy=300000
        )


    def test_add_car_ajax(self):
        self.client.login(username='admin', password='admin123')
        response = self.client.post(reverse('main:add_car'), {
            'brand': 'Toyota',
            'model': 'Avanza',
            'year': 2020,
            'price_cash': 100000000
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_delete_car_ajax(self):
        self.client.login(username='admin', password='admin123')
        car = Car.objects.create(showroom=self.showroom, brand="Toyota", model="Avanza")
        response = self.client.delete(reverse('main:delete_car', args=[car.id]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

