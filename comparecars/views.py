from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import CompareCarUser
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
            user_id = data.get('user_id')
            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            # Validasi user dan mobil
            user = get_object_or_404(User, id=user_id)
            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)

            # Membuat objek CompareCarUser
            comparison = CompareCarUser(user=user, car_one=car_one, car_two=car_two)
            comparison.save()

            return JsonResponse({'message': 'Comparison created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        # Ambil semua data mobil
        cars = Car.objects.all()

        # Ambil semua perbandingan mobil (jika diperlukan untuk keperluan lain)
        comparisons = CompareCarUser.objects.all()
        comparison_list = [
            {
                'id': comp.id,
                'user': comp.user.username,
                'car_one': comp.car_one.brand + " " + comp.car_one.model,
                'car_two': comp.car_two.brand + " " + comp.car_two.model
            }
            for comp in comparisons
        ]

        # Render HTML dan kirimkan daftar mobil ke template
        return render(request, 'compare.html', {'cars': cars, 'comparisons': comparison_list})

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@csrf_exempt
def compare_cars_with_id(request, id):
    comparison = get_object_or_404(CompareCarUser, id=id)

    if request.method == 'GET':
        # Menampilkan detail perbandingan mobil berdasarkan ID
        data = {
            'id': comparison.id,
            'user': comparison.user.username,
            'car_one': comparison.car_one.brand + " " + comparison.car_one.model,
            'car_two': comparison.car_two.brand + " " + comparison.car_two.model
        }
        return JsonResponse(data)

    elif request.method == 'DELETE':
        # Menghapus perbandingan mobil
        comparison.delete()
        return JsonResponse({'message': 'Comparison deleted successfully'}, status=204)

    elif request.method == 'PUT':
        try:
            # Parsing data dari PUT request untuk memperbarui perbandingan mobil
            data = json.loads(request.body)
            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)

            # Update comparison
            comparison.car_one = car_one
            comparison.car_two = car_two
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
    comparisons = CompareCarUser.objects.all()  # Atau filter berdasarkan user jika diperlukan
    return render(request, 'compare_list.html', {'comparisons': comparisons})