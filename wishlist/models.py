from django.db import models
from cars.models import Car  # Mengimpor model Car dari aplikasi 'cars'
from django.contrib.auth.models import User  # Mengimpor User untuk relasi foreign key

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Setiap pengguna memiliki wishlist sendiri
    car = models.ForeignKey(Car, on_delete=models.CASCADE)  # Mobil yang dimasukkan ke wishlist
    notes = models.TextField(blank=True, null=True)  # Catatan opsional untuk setiap mobil
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu ketika wishlist dibuat

    def __str__(self):
        return f'{self.user.username} - {self.car.name}'  # Mengembalikan string representasi dari wishlist
