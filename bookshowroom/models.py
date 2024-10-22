from django.db import models
import uuid 
from django.contrib.auth.models import User
from cars.models import ShowRoom
# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField()
    showroom = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)