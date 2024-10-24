# views.py di app main
from django.shortcuts import render, get_object_or_404
from cars.models import Car
from wishlist.models import Wishlist

def show_main(request):
    cars = Car.objects.all()
    print (cars)
    context = {
        'cars': cars,
        "user": request.user
    }
    return render(request, 'main.html', context)  # Render ke 'main/main.html'

def car_detail(request, car_id):
    car = Car.objects.get(pk=car_id)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists() if request.user.is_authenticated else False
    print(is_in_wishlist)
    context = { 
        'car': car,
        'showroom': car.showroom,  # The related showroom
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'car_detail.html', context)


