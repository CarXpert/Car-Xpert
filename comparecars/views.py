from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import CompareCarUser, CompareCar
from cars.models import Car
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def compare_cars(request):
    if request.method == 'POST':
        try:
            # Parsing data dari POST request
            data = json.loads(request.body)
            # user_id = data.get('user_id')
            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            # Validasi user dan mobil
            # user = get_object_or_404(User, id=user_id)
            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)

            # Membuat objek CompareCar dan CompareCarUser
            comparecar = CompareCar.objects.create(car1=car_one, car2=car_two)
            # comparison = CompareCarUser.objects.create(user=user, comparecar=comparecar)

            return JsonResponse({'message': 'Comparison created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        # Ambil semua data mobil
        cars = Car.objects.all()

        # Ambil semua perbandingan mobil
        comparisons = CompareCarUser.objects.all()
        return render(request, 'compare.html', {'cars': cars, 'comparisons': comparisons})

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def compare_cars_with_id(request, id):
    # Gunakan CompareCar, bukan CompareCarUser
    comparison = get_object_or_404(CompareCar, id=id)

    if request.method == 'GET':
        return render(request, 'view_compare.html', {
            'car1': comparison.car1,
            'car2': comparison.car2
        })

    elif request.method == 'DELETE':
        comparison.delete()
        return JsonResponse({'message': 'Comparison deleted successfully'}, status=204)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)

            comparison.car1 = car_one
            comparison.car2 = car_two
            comparison.save()

            return JsonResponse({'message': 'Comparison updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        return HttpResponseNotAllowed(['GET', 'DELETE', 'PUT'])

def get_cars(request):
    try:
        # Ambil semua data mobil
        cars = Car.objects.all()
        car_list = []
        for car in cars:
            car_list.append({
                'id': str(car.id),  # Pastikan UUID dikonversi ke string
                'brand': car.brand,
                'model': car.model,
                'year': car.year,
                'fuel_type': car.fuel_type,
                'color': car.color,
                'price_cash': car.price_cash,
            })
        return JsonResponse(car_list, safe=False)
    except Exception as e:
        # Jika terjadi error, log errornya dan kembalikan status 500
        return JsonResponse({'error': str(e)}, status=500)

def list_comparisons(request):
    # Cek apakah pengguna adalah anonymous user (belum login)
    # if request.user.is_authenticated:
    #     comparisons = CompareCar.objects.all()
    # else:
    #     comparisons = []  # Jika pengguna tidak login, beri daftar perbandingan kosong
    comparisons = CompareCar.objects.all()

    return render(request, 'compare_list.html', {'comparisons': comparisons})
