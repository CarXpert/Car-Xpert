from django.db import models
from django.contrib.auth.models import User  
from cars.models import Car 

class CompareCar(models.Model):
    car1 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='compare_car1')
    car2 = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='compare_car2')

    def __str__(self):
        return f"Compare: {self.car1.brand} vs {self.car2.brand}"

class CompareCarUser(models.Model):
    comparecar = models.ForeignKey(CompareCar, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Comparison of {self.comparecar.car1.brand} vs {self.comparecar.car2.brand}"
