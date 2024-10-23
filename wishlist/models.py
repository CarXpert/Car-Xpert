from django.db import models
from cars.models import Car  # Import Car model from app 'car'
from django.contrib.auth.models import User  # Import User for foreign key relation

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Each user has their own wishlist
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Car that is wishlisted
    notes = models.TextField(blank=True, null=True)  # Optional notes for each car
    created_at = models.DateTimeField(auto_now_add=True)
