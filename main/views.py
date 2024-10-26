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
