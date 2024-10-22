from django.db import models
import uuid

class ShowRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showroom_name = models.CharField(max_length=30)
    showroom_location = models.TextField()
    showroom_regency = models.CharField(max_length=30)


class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    showroom = models.ForeignKey(ShowRoom, on_delete=models.CASCADE)
    ucd_id = models.IntegerField()
    brand = models.CharField(max_length=30)
    car_type = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=30)
    year = models.PositiveIntegerField()
    transmission = models.CharField(max_length=30)
    fuel_type = models.CharField(max_length=30)
    doors = models.PositiveIntegerField()
    cylinder_size = models.PositiveIntegerField()
    cylinder_total = models.PositiveIntegerField()
    turbo = models.BooleanField()
    mileage = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=30)
    price_cash = models.PositiveIntegerField()
    price_credit = models.PositiveIntegerField()
    pkb_value = models.PositiveIntegerField()
    pkb_base = models.PositiveIntegerField()
    stnk_date = models.DateField()
    levy_date = models.DateField()
    swdkllj = models.PositiveIntegerField()
    total_levy = models.PositiveIntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

 

