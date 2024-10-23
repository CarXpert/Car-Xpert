from django.db import models
from cars.models import Car 
from django.contrib.auth.models import User

class CompareCarUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car_one = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comparecaruser_car_one')
    car_two = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comparecaruser_car_two')
