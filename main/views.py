# views.py di app main
from django.shortcuts import render, get_object_or_404, redirect
from cars.models import Car, ShowRoom
from wishlist.models import Wishlist
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils import timezone
from .forms import CarEditForm
from .forms import AddCarForm
from news.models import NewsArticle 
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
    news = NewsArticle.objects.all().order_by('-published_date')[:3]  # Get the latest 3 news articles
    context = {
        'cars': cars,
        'news': news,  
        'user': request.user
    }
    return render(request, 'main.html', context)  

def landing_page(request):
    return render(request, 'landing_page.html')

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)  # Use get_object_or_404 for better error handling
    is_in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists() if request.user.is_authenticated else False
    context = { 
        'car': car,
        'showroom': car.showroom,  # The related showroom
        'is_in_wishlist': is_in_wishlist,
        'user': request.user  # Pass user to the template
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

from django.http import JsonResponse
from django.db.models import Q

def get_cars_filtered(request, query):
    # Split query into words by spaces
    query_words = query.split()
    
    # Build the filter for each word
    filters = Q()
    for word in query_words:
        word_filter = (
            Q(brand__icontains=word) |
            Q(car_type__icontains=word) |
            Q(model__icontains=word) |
            Q(color__icontains=word) |
            Q(transmission__icontains=word) |
            Q(fuel_type__icontains=word) |
            Q(license_plate__icontains=word) |
            Q(showroom__showroom_name__icontains=word) |
            Q(showroom__showroom_location__icontains=word) |
            Q(showroom__showroom_regency__icontains=word)
        )
        filters &= word_filter  # Combine filters with AND for each word

    # Retrieve cars that match all words
    cars = Car.objects.filter(filters)

    # Prepare data for JSON response
    cars_data = [{
        "id": str(car.id),
        "brand": car.brand,
        "car_type": car.car_type,
        "model": car.model,
        "color": car.color,
        "year": car.year,
        "transmission": car.transmission,
        "fuel_type": car.fuel_type,
        "doors": car.doors,
        "cylinder_size": car.cylinder_size,
        "cylinder_total": car.cylinder_total,
        "turbo": car.turbo,
        "mileage": car.mileage,
        "license_plate": car.license_plate,
        "price_cash": car.price_cash,
        "price_credit": car.price_credit,
        "pkb_value": car.pkb_value,
        "pkb_base": car.pkb_base,
        "stnk_date": car.stnk_date.isoformat(),
        "levy_date": car.levy_date.isoformat(),
        "swdkllj": car.swdkllj,
        "total_levy": car.total_levy,
        "created_at": car.created_at.isoformat(),
        "updated_at": car.updated_at.isoformat(),
        "showroom": {
            "name": car.showroom.showroom_name,
            "location": car.showroom.showroom_location,
            "regency": car.showroom.showroom_regency
        }
    } for car in cars]

    # Return JSON response
    return JsonResponse({"cars": cars_data, "query": query}, safe=False)

