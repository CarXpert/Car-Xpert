# views.py di app main
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Car, ShowRoom
from wishlist.models import Wishlist
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .forms import CarEditForm



def main_view(request):
    cars = Car.objects.all()  # Retrieve all cars from the database
    return render(request, 'main.html', {'cars': cars})  # Pass cars to the template

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

# Ensure only staff members (admins) can access this view
@user_passes_test(lambda u: u.is_staff)
def edit_car_view(request, car_id):
    # Fetch the car instance or return a 404 if not found
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        # Bind form with POST data
        form = CarEditForm(request.POST, instance=car)
        if form.is_valid():
            form.save()  # Save changes to the car instance
            return redirect('main:car_detail', car_id=car.id)  # Redirect to car_detail after save
    else:
        # For GET requests, populate the form with the car's existing data
        form = CarEditForm(instance=car)

    return render(request, 'edit_car.html', {'form': form, 'car': car})