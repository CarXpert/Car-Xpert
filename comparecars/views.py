from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseNotAllowed
from .models import CompareCarUser, CompareCar
from django.urls import reverse
from cars.models import Car
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.core import serializers
from django.http import HttpResponse
from .models import CompareCarUser
import logging
from django.contrib.auth.models import AnonymousUser

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
        cars = Car.objects.all()
        car_list = []
        for car in cars:
            car_list.append({
                'id': str(car.id),  
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
            comparison = get_object_or_404(CompareCarUser, id=id, user=request.user)
            comparison.comparecar.title = new_title
            comparison.comparecar.save()

            return JsonResponse({'message': 'Title updated successfully'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
def show_comparison_json(request):
    try:
        # Ambil semua perbandingan milik pengguna yang sedang login
        comparisons = CompareCarUser.objects.filter(user=request.user)
        data = []
        
        for comparison in comparisons:
            data.append({
                'id': comparison.id,
                'title': comparison.comparecar.title,
                'date_added': comparison.comparecar.date_added,
                'car1': {
                    'id': comparison.comparecar.car1.id,
                    'brand': comparison.comparecar.car1.brand,
                    'model': comparison.comparecar.car1.model,
                    'year': comparison.comparecar.car1.year,
                    'fuel_type': comparison.comparecar.car1.fuel_type,
                    'color': comparison.comparecar.car1.color,
                    'price_cash': comparison.comparecar.car1.price_cash,
                },
                'car2': {
                    'id': comparison.comparecar.car2.id,
                    'brand': comparison.comparecar.car2.brand,
                    'model': comparison.comparecar.car2.model,
                    'year': comparison.comparecar.car2.year,
                    'fuel_type': comparison.comparecar.car2.fuel_type,
                    'color': comparison.comparecar.car2.color,
                    'price_cash': comparison.comparecar.car2.price_cash,
                },
            })
        
        return JsonResponse(data, safe=False, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


logger = logging.getLogger(__name__)

#@login_required
def list_comparisons_json(request):
    try:
        # Validasi pengguna
        if isinstance(request.user, AnonymousUser):
            logger.error("User is not authenticated.")
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        # Ambil data dari database
        comparisons = CompareCarUser.objects.filter(user=request.user)
        logger.info(f"User: {request.user}, Comparisons Count: {comparisons.count()}")

        res_data = []
        for comparison in comparisons:
            try:
                comparecar = comparison.comparecar
                logger.info(f"Processing comparison ID: {comparison.pk}")

                car1_brand = comparecar.car1.brand if comparecar.car1 else "Unknown"
                car1_model = comparecar.car1.model if comparecar.car1 else "Unknown"
                car2_brand = comparecar.car2.brand if comparecar.car2 else "Unknown"
                car2_model = comparecar.car2.model if comparecar.car2 else "Unknown"
                date_added = comparecar.date_added.strftime('%Y-%m-%d %H:%M:%S') if comparecar.date_added else "Unknown"

                res_data.append({
                    'id': comparison.pk,
                    'title': comparecar.title or 'Untitled Comparison',
                    'car1': {'brand': car1_brand, 'model': car1_model},
                    'car2': {'brand': car2_brand, 'model': car2_model},
                    'date_added': date_added,
                })

            except Exception as e:
                logger.error(f"Error processing comparison ID {comparison.pk}: {e}")

        return JsonResponse(res_data, safe=False)

    except Exception as e:
        logger.error(f"Error in list_comparisons_json: {e}")
        return JsonResponse({'error': 'Something went wrong while processing the request.'}, status=500)
