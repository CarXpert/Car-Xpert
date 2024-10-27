# views.py di app main
from django.shortcuts import render, get_object_or_404
from cars.models import Car
from wishlist.models import Wishlist
from news.models import NewsArticle 

def show_main(request):
    cars = Car.objects.all()
    news = NewsArticle.objects.all().order_by('-published_date')[:3]  # Ambil berita terbaru, maksimal 3 berita
    context = {
        'cars': cars,
        'news': news,  
        'user': request.user
    }
    return render(request, 'main.html', context)  

def landing_page(request):
    return render(request, 'landing_page.html')

def car_detail(request, car_id):
    car = Car.objects.get(pk=car_id)
    is_in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists() if request.user.is_authenticated else False
    context = { 
        'car': car,
        'showroom': car.showroom,  # The related showroom
        'is_in_wishlist': is_in_wishlist,
    }
    return render(request, 'car_detail.html', context)

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

