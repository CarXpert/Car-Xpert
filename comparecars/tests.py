from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cars.models import Car, ShowRoom
from .models import CompareCar, CompareCarUser
import json
from datetime import datetime

class CompareCarsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

        self.showroom = ShowRoom.objects.create(
            showroom_name="ARJUNA MOTOR DEALER MOBIL BEKAS",
            showroom_location="Jl raya jatiwaringin no 2 pangkalan jati kalimalang Jakarta timur",
            showroom_regency="Jakarta Timur"
        )

        self.car1 = Car.objects.create(
            showroom=self.showroom,
            brand="Jeep",
            car_type="GRAND CHEROKEE 5.7AT",
            model="JEEP L.C.HDTP",
            color="ABU ABU",
            year=2011,
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=5654,
            cylinder_total=8,
            turbo=False,
            mileage=45000,
            license_plate="B 1526 PJG",
            price_cash=425000000,
            price_credit=440000000,
            pkb_value=511000000,
            pkb_base=10731000,
            stnk_date=datetime.strptime("2023-11-01", "%Y-%m-%d"),
            levy_date=datetime.strptime("2022-11-01", "%Y-%m-%d"),
            swdkllj=143000,
            total_levy=12231800
        )

        self.car2 = Car.objects.create(
            showroom=self.showroom,
            brand="Range Rover",
            car_type="RANGE ROVER 4.2L V8 AT",
            model="JEEP S.C.HDTP",
            color="HITAM",
            year=2007,
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=5,
            cylinder_size=4187,
            cylinder_total=8,
            turbo=False,
            mileage=95,
            license_plate="B 2907 SXV",
            price_cash=535000000,
            price_credit=550000000,
            pkb_value=536000000,
            pkb_base=11256000,
            stnk_date=datetime.strptime("2024-10-16", "%Y-%m-%d"),
            levy_date=datetime.strptime("2023-10-16", "%Y-%m-%d"),
            swdkllj=143000,
            total_levy=11399000
        )

        self.compare_cars_url = reverse('compare_cars')
        self.compare_cars_with_id_url = lambda id: reverse('compare_cars_with_id', args=[id])
        self.list_comparisons_url = reverse('list_comparisons')
        self.edit_comparison_title_url = lambda id: reverse('edit_comparison_title', args=[id])

    def test_compare_cars_post(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.compare_cars_url, json.dumps({
            'car_one_id': str(self.car1.id), 
            'car_two_id': str(self.car2.id)  
        }), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertIn('Comparison created successfully', response.json().get('message'))
        self.assertTrue(CompareCar.objects.exists())
        self.assertTrue(CompareCarUser.objects.exists())

    def test_compare_cars_post_invalid_data(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(self.compare_cars_url, json.dumps({
            'car_one_id': 'invalid_id', 
            'car_two_id': str(self.car2.id)  
        }), content_type="application/json")
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_compare_cars_get(self):
        response = self.client.get(self.compare_cars_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compare.html')
        self.assertIn('cars', response.context)
        self.assertIn('comparisons', response.context)

    def test_compare_cars_with_id_get(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        CompareCarUser.objects.create(comparecar=comparecar, user=self.user)
        
        response = self.client.get(self.compare_cars_with_id_url(comparecar.id))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_compare.html')
        self.assertEqual(response.context['car1'], self.car1)
        self.assertEqual(response.context['car2'], self.car2)

    def test_compare_cars_with_id_put(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        CompareCarUser.objects.create(comparecar=comparecar, user=self.user)

        response = self.client.put(self.compare_cars_with_id_url(comparecar.id), json.dumps({
            'car_one_id': str(self.car2.id), 
            'car_two_id': str(self.car1.id)
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Comparison updated successfully', response.json().get('message'))
        comparecar.refresh_from_db()
        self.assertEqual(comparecar.car1, self.car2)
        self.assertEqual(comparecar.car2, self.car1)

    def test_compare_cars_with_id_put_invalid_data(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        CompareCarUser.objects.create(comparecar=comparecar, user=self.user)

        response = self.client.put(self.compare_cars_with_id_url(comparecar.id), json.dumps({
            'car_one_id': 'invalid_id'
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_compare_cars_with_id_delete(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        CompareCarUser.objects.create(comparecar=comparecar, user=self.user)
        
        response = self.client.delete(self.compare_cars_with_id_url(comparecar.id))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(CompareCar.objects.exists())

    def test_get_cars(self):
        response = self.client.get(reverse('get_cars'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['brand'], "Jeep")

    def test_list_comparisons(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        CompareCarUser.objects.create(comparecar=comparecar, user=self.user)
        
        response = self.client.get(self.list_comparisons_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compare_list.html')
        self.assertIn('comparisons', response.context)

    def test_edit_comparison_title(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        comparison_user = CompareCarUser.objects.create(comparecar=comparecar, user=self.user)

        response = self.client.put(self.edit_comparison_title_url(comparison_user.id), json.dumps({
            'title': 'Updated Title'
        }), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertIn('Title updated successfully', response.json().get('message'))
        comparecar.refresh_from_db()
        self.assertEqual(comparecar.title, 'Updated Title')

    def test_edit_comparison_title_no_title(self):
        self.client.login(username='testuser', password='password')
        comparecar = CompareCar.objects.create(car1=self.car1, car2=self.car2)
        comparison_user = CompareCarUser.objects.create(comparecar=comparecar, user=self.user)

        response = self.client.put(self.edit_comparison_title_url(comparison_user.id), json.dumps({
        }), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

