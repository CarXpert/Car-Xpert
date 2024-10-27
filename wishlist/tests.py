from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Wishlist, Car
from .forms import WishlistNoteForm

class WishlistModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Menggunakan field model yang benar
        self.car = Car.objects.create(id=1, showroom=None, brand='Test Brand', car_type='SUV',
                                      model='Test Car', color='Red', year=2020,
                                      transmission='Automatic', fuel_type='Petrol',
                                      doors=4, cylinder_size=2000, cylinder_total=4,
                                      turbo=False, mileage=10000, license_plate='B 1234 XYZ',
                                      price_cash=200000000, price_credit=210000000,
                                      pkb_value=5000000, pkb_base=5000000,
                                      stnk_date='2024-01-01', levy_date='2024-01-01',
                                      swdkllj=1000000, total_levy=6000000,
                                      created_at='2024-10-27T10:00:00Z', updated_at='2024-10-27T10:00:00Z')
        self.wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes='Test note')

    def test_wishlist_str(self):
        self.assertEqual(str(self.wishlist_item), 'testuser - Test Car')

    def test_wishlist_creation(self):
        self.assertIsInstance(self.wishlist_item, Wishlist)
        self.assertEqual(self.wishlist_item.notes, 'Test note')
        self.assertEqual(self.wishlist_item.user.username, 'testuser')
        self.assertEqual(self.wishlist_item.car.model, 'Test Car')

class WishlistViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(id=1, showroom=None, brand='Test Brand', car_type='SUV',
                                      model='Test Car', color='Red', year=2020,
                                      transmission='Automatic', fuel_type='Petrol',
                                      doors=4, cylinder_size=2000, cylinder_total=4,
                                      turbo=False, mileage=10000, license_plate='B 1234 XYZ',
                                      price_cash=200000000, price_credit=210000000,
                                      pkb_value=5000000, pkb_base=5000000,
                                      stnk_date='2024-01-01', levy_date='2024-01-01',
                                      swdkllj=1000000, total_levy=6000000,
                                      created_at='2024-10-27T10:00:00Z', updated_at='2024-10-27T10:00:00Z')
        self.client.login(username='testuser', password='testpassword')

    def test_show_wishlist(self):
        Wishlist.objects.create(user=self.user, car=self.car)
        response = self.client.get(reverse('wishlist:wishlist_view'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Car')

    def test_add_remove_wishlist(self):
        response = self.client.post(reverse('wishlist:add_remove_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'in_wishlist': True, 'message': 'Wishlist updated successfully.'})

        self.assertTrue(Wishlist.objects.filter(user=self.user, car=self.car).exists())

        response = self.client.post(reverse('wishlist:add_remove_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'in_wishlist': False, 'message': 'Wishlist updated successfully.'})

        self.assertFalse(Wishlist.objects.filter(user=self.user, car=self.car).exists())

    def test_remove_from_wishlist(self):
        wishlist_item = Wishlist.objects.create(user=self.user, car=self.car)
        response = self.client.post(reverse('wishlist:remove_from_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Item removed from wishlist.'})
        self.assertFalse(Wishlist.objects.filter(id=wishlist_item.id).exists())

    def test_check_wishlist(self):
        Wishlist.objects.create(user=self.user, car=self.car, notes='Test note')
        response = self.client.get(reverse('wishlist:check_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'in_wishlist': True, 'note': 'Test note'})

    def test_edit_note_success(self):
        wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes='Old note')
        response = self.client.post(reverse('wishlist:edit_note', args=[wishlist_item.pk]), {'notes': 'Updated note'})
        self.assertRedirects(response, reverse('wishlist:wishlist_view'))  # Pastikan URL ini benar
        wishlist_item.refresh_from_db()
        self.assertEqual(wishlist_item.notes, 'Updated note')

    def test_edit_note_failure(self):
        wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes='Old note')
        response = self.client.post(reverse('wishlist:edit_note', args=[wishlist_item.pk]), {'notes': ''})
        self.assertEqual(response.status_code, 200)  # Masih dalam proses, tidak redirect
        self.assertContains(response, 'This field is required.')  # Sesuaikan dengan pesan kesalahan form

    def test_wishlist_view_url_exists(self):
        response = self.client.get(reverse('wishlist:wishlist_view'))
        self.assertEqual(response.status_code, 200)

    def test_add_remove_wishlist_url_exists(self):
        response = self.client.post(reverse('wishlist:add_remove_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)

    def test_remove_from_wishlist_url_exists(self):
        wishlist_item = Wishlist.objects.create(user=self.user, car=self.car)
        response = self.client.post(reverse('wishlist:remove_from_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)

    def test_check_wishlist_url_exists(self):
        response = self.client.get(reverse('wishlist:check_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)

    def test_edit_note_url_exists(self):
        wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes='Old note')
        response = self.client.get(reverse('wishlist:edit_note', args=[wishlist_item.pk]))
        self.assertEqual(response.status_code, 200)

class WishlistFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.car = Car.objects.create(id=1, showroom=None, brand='Test Brand', car_type='SUV',
                                      model='Test Car', color='Red', year=2020,
                                      transmission='Automatic', fuel_type='Petrol',
                                      doors=4, cylinder_size=2000, cylinder_total=4,
                                      turbo=False, mileage=10000, license_plate='B 1234 XYZ',
                                      price_cash=200000000, price_credit=210000000,
                                      pkb_value=5000000, pkb_base=5000000,
                                      stnk_date='2024-01-01', levy_date='2024-01-01',
                                      swdkllj=1000000, total_levy=6000000,
                                      created_at='2024-10-27T10:00:00Z', updated_at='2024-10-27T10:00:00Z')
        self.wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes='Old note')

    def test_wishlist_note_form_valid(self):
        form_data = {'notes': 'New note'}
        form = WishlistNoteForm(data=form_data, instance=self.wishlist_item)
        self.assertTrue(form.is_valid())

    def test_wishlist_note_form_invalid(self):
        form_data = {'notes': ''}
        form = WishlistNoteForm(data=form_data, instance=self.wishlist_item)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)  # Pastikan ada satu kesalahan
