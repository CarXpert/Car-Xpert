# views.py di app main
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Car, ShowRoom
from wishlist.models import Wishlist
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from .forms import CarEditForm
from .forms import AddCarForm
from django.http import JsonResponse
import json
import os
from django.conf import settings



def main_view(request):
    # Path ke file showrooms.json
    showroom_file_path = os.path.join(settings.BASE_DIR, 'cars', 'fixtures', 'showrooms.json')

    # Debugging: Cek apakah file path benar
    print("Showroom file path:", showroom_file_path)
    
    # Load data dari showrooms.json
    try:
        with open(showroom_file_path, 'r') as f:
            showrooms_data = json.load(f)
            print("Showrooms data loaded:", showrooms_data)  # Debugging: Cek data
    except Exception as e:
        print("Error loading showrooms.json:", e)
        showrooms_data = []

    # Kirim data showroom ke template main.html
    return render(request, 'main.html', {'showrooms': showrooms_data})

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

login_required
def add_car(request):
    if request.method == 'POST' and request.user.is_staff:
        form = AddCarForm(request.POST)
        if form.is_valid():
            car = form.save(commit=False)
            showroom_id = request.POST.get('showroom_id')  # Ambil showroom_id dari form
            car.showroom = ShowRoom.objects.get(id=showroom_id)  # Hubungkan ke showroom
            car.created_at = timezone.now()
            car.updated_at = timezone.now()
            car.save()
            return JsonResponse({'success': True})

    return JsonResponse({'success': False})