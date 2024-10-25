from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import CompareCarUser, CompareCar
from django.urls import reverse
from cars.models import Car
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt

def compare_cars(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)
            comparecar = CompareCar.objects.create(car1=car_one, car2=car_two)
            CompareCarUser.objects.create(comparecar=comparecar, user=request.user)

            return JsonResponse({'message': 'Comparison created successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == 'GET':
        cars = Car.objects.all()
        comparisons = CompareCar.objects.all()
        return render(request, 'compare.html', {'cars': cars, 'comparisons': comparisons})

    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@login_required
@csrf_exempt
def compare_cars_with_id(request, id):
    comparison = get_object_or_404(CompareCarUser, id=id, user=request.user)

    if request.method == 'GET':
        return render(request, 'view_compare.html', {
            'car1': comparison.comparecar.car1,
            'car2': comparison.comparecar.car2
        })

    elif request.method == 'DELETE':
        comparison.comparecar.delete()
        return JsonResponse({'message': 'Comparison deleted successfully'}, status=204)

    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
            title = data.get('title', None)
            if title is not None:
                comparison.comparecar.title = title
                comparison.comparecar.save()
                return JsonResponse({'message': 'Comparison title updated successfully'}, status=200)

            car_one_id = data.get('car_one_id')
            car_two_id = data.get('car_two_id')

            car_one = get_object_or_404(Car, id=car_one_id)
            car_two = get_object_or_404(Car, id=car_two_id)

            comparison.comparecar.car1 = car_one
            comparison.comparecar.car2 = car_two
            comparison.comparecar.save()

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
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='/auth/login/')
def list_comparisons(request):
    sort_order = request.GET.get('sort', 'newest')  
    comparisons = CompareCarUser.objects.filter(user=request.user)

    if sort_order == 'newest':
        comparisons = comparisons.order_by('-comparecar__date_added') 
    elif sort_order == 'oldest':
        comparisons = comparisons.order_by('comparecar__date_added') 

    return render(request, 'compare_list.html', {'comparisons': comparisons, 'sort_order': sort_order})


@csrf_exempt
def edit_comparison_title(request, id):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            new_title = data.get('title')

            if not new_title:
                return JsonResponse({'error': 'No title provided'}, status=400)

            # Ambil comparison dan update title
            comparison = get_object_or_404(CompareCarUser, id=id, user=request.user)
            comparison.comparecar.title = new_title
            comparison.comparecar.save()

            return JsonResponse({'message': 'Title updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)