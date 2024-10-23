# views.py di app cars_detail
from django.shortcuts import render, get_object_or_404
from .models import Car

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    context = {
        'car': car,
    }
    return render(request, 'cars_detail/car_detail.html', context)
