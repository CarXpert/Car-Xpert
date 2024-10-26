from django.shortcuts import render, get_object_or_404
from cars.models import Car
from wishlist.models import Wishlist
from news.models import NewsArticle 

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
