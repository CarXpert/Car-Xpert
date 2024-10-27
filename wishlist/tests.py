from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from cars.models import Car, ShowRoom
from wishlist.models import Wishlist
from wishlist.views import show_wishlist, add_remove_wishlist, remove_from_wishlist, edit_note

class WishlistModelTest(TestCase):
    def setUp(self):
        self.showroom = ShowRoom.objects.create(
            showroom_name='Test Showroom',
            showroom_location='Test Location',
            showroom_regency='Test Regency'
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.car = Car.objects.create(
            model="Test Car",
            brand="Test Brand",
            year=2020,
            showroom=self.showroom,
            car_type="Sedan",
            color="Red",
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=22000,
            pkb_value=1500.0,
            pkb_base=1200.0,
            stnk_date="2022-01-01",
            levy_date="2022-01-01",
            swdkllj=300.0,
            total_levy=500.0,
        )
        self.wishlist_item = Wishlist.objects.create(user=self.user, car=self.car, notes="My Test Note")

    def test_wishlist_str(self):
        self.assertEqual(str(self.wishlist_item), f"{self.user} - {self.car.model}")

    def test_wishlist_notes(self):
        self.assertEqual(self.wishlist_item.notes, "My Test Note")

class ShowWishlistViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.showroom = ShowRoom.objects.create(
            showroom_name='Test Showroom',
            showroom_location='Test Location',
            showroom_regency='Test Regency'
        )
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.car = Car.objects.create(
            model="Test Car",
            brand="Test Brand",
            year=2020,
            showroom=cls.showroom,
            car_type="Sedan",
            color="Red",
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=22000,
            pkb_value=1500.0,
            pkb_base=1200.0,
            stnk_date="2022-01-01",
            levy_date="2022-01-01",
            swdkllj=300.0,
            total_levy=500.0,
        )
        cls.wishlist_item = Wishlist.objects.create(user=cls.user, car=cls.car, notes="My Test Note")

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_show_wishlist_view(self):
        response = self.client.get(reverse('wishlist:wishlist_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist/wishlist_page.html')
        self.assertContains(response, "Test Car")
        self.assertContains(response, "My Test Note")

class AddRemoveWishlistViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.showroom = ShowRoom.objects.create(
            showroom_name='Test Showroom',
            showroom_location='Test Location',
            showroom_regency='Test Regency'
        )
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.car = Car.objects.create(
            model="Test Car",
            brand="Test Brand",
            year=2020,
            showroom=cls.showroom,
            car_type="Sedan",
            color="Red",
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=22000,
            pkb_value=1500.0,
            pkb_base=1200.0,
            stnk_date="2022-01-01",
            levy_date="2022-01-01",
            swdkllj=300.0,
            total_levy=500.0,
        )

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_add_to_wishlist(self):
        response = self.client.post(reverse('wishlist:add_remove_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Wishlist.objects.filter(user=self.user, car=self.car).exists())
        self.assertJSONEqual(response.content, {'in_wishlist': True, 'message': 'Wishlist updated successfully.'})

    def test_remove_from_wishlist(self):
        Wishlist.objects.create(user=self.user, car=self.car)
        response = self.client.post(reverse('wishlist:add_remove_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Wishlist.objects.filter(user=self.user, car=self.car).exists())
        self.assertJSONEqual(response.content, {'in_wishlist': False, 'message': 'Wishlist updated successfully.'})

class RemoveFromWishlistViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.showroom = ShowRoom.objects.create(
            showroom_name='Test Showroom',
            showroom_location='Test Location',
            showroom_regency='Test Regency'
        )
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.car = Car.objects.create(
            model="Test Car",
            brand="Test Brand",
            year=2020,  # Provide a year value
            showroom=cls.showroom,  # Assuming you need to set this appropriately
            car_type="Sedan",
            color="Red",
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=22000,
            pkb_value=1500.0,
            pkb_base=1200.0,
            stnk_date="2022-01-01",
            levy_date="2022-01-01",
            swdkllj=300.0,
            total_levy=500.0,
        )
        cls.wishlist_item = Wishlist.objects.create(user=cls.user, car=cls.car)

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_remove_wishlist_item(self):
        response = self.client.post(reverse('wishlist:remove_from_wishlist'), {'car_id': self.car.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Wishlist.objects.filter(user=self.user, car=self.car).exists())
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Item removed from wishlist.'})

class EditNoteViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.showroom = ShowRoom.objects.create(
            showroom_name='Test Showroom',
            showroom_location='Test Location',
            showroom_regency='Test Regency'
        )
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.car = Car.objects.create(
            model="Test Car",
            brand="Test Brand",
            year=2020,
            showroom=cls.showroom,  
            car_type="Sedan",
            color="Red",
            transmission="Automatic",
            fuel_type="Gasoline",
            doors=4,
            cylinder_size=2.0,
            cylinder_total=4,
            turbo=False,
            mileage=10000,
            license_plate="ABC123",
            price_cash=20000,
            price_credit=22000,
            pkb_value=1500.0,
            pkb_base=1200.0,
            stnk_date="2022-01-01",
            levy_date="2022-01-01",
            swdkllj=300.0,
            total_levy=500.0,
        )
        cls.wishlist_item = Wishlist.objects.create(user=cls.user, car=cls.car, notes="Old Note")

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_edit_note_view(self):
        response = self.client.post(reverse('wishlist:edit_note', args=[self.wishlist_item.id]), {'notes': 'Updated Note'})
        self.assertEqual(response.status_code, 302)  
        self.wishlist_item.refresh_from_db()
        self.assertEqual(self.wishlist_item.notes, "Updated Note")

class WishlistURLTest(TestCase):
    def test_show_wishlist_url_resolves(self):
        url = reverse('wishlist:wishlist_view')
        self.assertEqual(resolve(url).func, show_wishlist)

    def test_add_remove_wishlist_url_resolves(self):
        url = reverse('wishlist:add_remove_wishlist')
        self.assertEqual(resolve(url).func, add_remove_wishlist)

    def test_remove_from_wishlist_url_resolves(self):
        url = reverse('wishlist:remove_from_wishlist')
        self.assertEqual(resolve(url).func, remove_from_wishlist)

    def test_edit_note_url_resolves(self):
        url = reverse('wishlist:edit_note', args=[1])
        self.assertEqual(resolve(url).func, edit_note)
