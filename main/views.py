# views.py di app main
from django.shortcuts import render
from .models import Car


def car_list(request):
    cars = Car.objects.all()  # Mengambil semua mobil dari database
    context = {
        'cars': cars,
    }
    return render(request, 'main/main.html', context)  # Render ke 'main/main.html'

