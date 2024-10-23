from django.db import models
from django.contrib.auth.models import User
from wishlist.models import Wishlist
from comparecars.models import CompareCarUser
from bookshowroom.models import Booking

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=10)
    wishlist = models.ManyToManyField(Wishlist, related_name="wishlist")
    comparecars = models.ManyToManyField(CompareCarUser, related_name="comparecars")
    bookshowroom = models.ManyToManyField(Booking, related_name="bookshowroom")
