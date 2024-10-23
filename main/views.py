# views.py di app main
from django.shortcuts import render
from .models import Car

# def show_main(request):
#     context = {"user": request.user}
#     return render(request, "main.html", context)

# def car_list(request):
#     cars = Car.objects.all()  # Mengambil semua mobil dari database
#     context = {
#         'cars': cars,
#     }
#     return render(request, 'main/main.html', context)  # Render ke 'main/main.html'

def show_main(request):
    cars = Car.objects.all()
    print (cars)

    context = {
        'cars': cars,
        "user": request.user
    }
    return render(request, 'main.html', context)  # Render ke 'main/main.html'


