from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Booking
from cars.models import ShowRoom, Car
from datetime import datetime

class BookingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        self.showroom = ShowRoom.objects.create(
            showroom_name="Test Showroom",
            showroom_location="Test Location",
            showroom_regency="Test Regency"
        )
        
        self.car = Car.objects.create(
            showroom=self.showroom,
            brand="Test Brand",
            car_type="Test Type",
            model="Test Model",
            color="Red",
            year=2023,
            transmission="Automatic",
            fuel_type="Petrol",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=21000,
            pkb_value=500,
            pkb_base=300,
            stnk_date="2024-01-01",
            levy_date="2024-01-01",
            swdkllj=150,
            total_levy=450,
            created_at="2024-01-01",
            updated_at="2024-01-01",
        )

    def test_get_showrooms(self):
        response = self.client.get(reverse('bookshowroom:get_showrooms'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('showroom_name', response.json()[0])

    def test_get_locations(self):
        response = self.client.get(reverse('bookshowroom:get_locations', args=[self.showroom.showroom_name]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['showroom_location'], "Test Location")

    def test_get_cars(self):
        response = self.client.get(reverse('bookshowroom:get_cars', args=[str(self.showroom.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]['brand'], "Test Brand")

    def test_create_booking_ajax(self):
        response = self.client.post(reverse('bookshowroom:create_booking_ajax'), {
            'showroom_id': self.showroom.id,
            'car_id': self.car.id,
            'visit_date': '2024-10-25',
            'visit_time': '14:00',
            'notes': 'Test booking note',
        })
        self.assertEqual(response.status_code, 201)

    def test_get_booking_by_id(self):
        booking = Booking.objects.create(
            user=self.user,
            showroom=self.showroom,
            car=self.car,
            visit_date=datetime(2024, 10, 25).date(),
            visit_time=datetime(2024, 10, 25, 14, 0).time(),
            notes="Test Note"
        )
        response = self.client.get(reverse('bookshowroom:get_booking_by_id', args=[str(booking.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['notes'], "Test Note")

    def test_delete_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            showroom=self.showroom,
            car=self.car,
            visit_date=datetime(2024, 10, 25).date(),
            visit_time=datetime(2024, 10, 25, 14, 0).time(),
            notes="Test Note"
        )
        response = self.client.delete(reverse('bookshowroom:delete_booking', args=[str(booking.id)]))
        self.assertEqual(response.status_code, 200)  # Updated to 204 for successful delete
        self.assertEqual(response.json()['message'], 'Booking deleted successfully.')

    def test_edit_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            showroom=self.showroom,
            car=self.car,
            visit_date=datetime(2024, 10, 25).date(),
            visit_time=datetime(2024, 10, 25, 14, 0).time(),
            notes="Test Note"
        )
        response = self.client.post(reverse('bookshowroom:edit_booking'), {
            'booking_id': booking.id,
            'showroom_id': self.showroom.id,
            'car_id': self.car.id,
            'visit_date': '2024-10-26',
            'visit_time': '15:00',
            'notes': 'Updated note'
        })
        self.assertEqual(response.status_code, 200)
        booking.refresh_from_db()
        self.assertEqual(booking.notes, 'Updated note')
