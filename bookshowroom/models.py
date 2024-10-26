from django.db import models
import uuid 
from django.contrib.auth.models import User
from cars.models import ShowRoom, Car
# Create your models here.
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showroom = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE )
    visit_date = models.DateField(default='2024-01-01')
    visit_time = models.TimeField(default='12:00:00')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)  