from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags

# Create your views here.
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from .models import Booking
from cars.models import ShowRoom, Car
from bookshowroom.models import Booking
from django.contrib.auth.models import User
from datetime import datetime
from django.core import serializers
from django.http import JsonResponse
import uuid
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/auth/login/')
def show_booking(request):
    context = {
        'user': request.user,
    }

    return render(request, "booking.html", context)


def get_showrooms(request):
    showrooms = ShowRoom.objects.values('showroom_name', 'showroom_regency', 'showroom_location')
    unique_showrooms = []
    seen_names = set()

    for showroom in showrooms:
        if showroom['showroom_name'] not in seen_names:
            unique_showrooms.append(showroom)
            seen_names.add(showroom['showroom_name'])

    return JsonResponse(unique_showrooms, safe=False)



def get_locations(request, showroom_name):
    locations = ShowRoom.objects.filter(showroom_name=showroom_name).values('id', 'showroom_name', 'showroom_location', 'showroom_regency')
    location_list = list(locations)  
    return JsonResponse(location_list, safe=False)


def get_cars(request, showroom_id_str):
    try:
        showroom_id = uuid.UUID(showroom_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)

    cars = Car.objects.filter(showroom__id=showroom_id).values(
        'id', 'brand', 'car_type', 'model', 'color', 
        'year', 'transmission', 'fuel_type', 'doors', 
        'cylinder_size', 'cylinder_total', 'turbo', 
        'mileage', 'license_plate', 'price_cash', 
        'price_credit', 'pkb_value', 'pkb_base', 
        'stnk_date', 'levy_date', 'swdkllj', 
        'total_levy', 'created_at', 'updated_at'
    )
    
    car_list = list(cars)  
    return JsonResponse(car_list, safe=False)


@login_required(login_url='/auth/login/')
def get_bookings(request):
    data = Booking.objects.select_related('user', 'showroom', 'car').filter(user=request.user)
    bookings = []
    for booking in data:
        bookings.append({
            'id': booking.id,
            'user': {
                'id': booking.user.id,
                'username': booking.user.username,
            },
            'showroom': {
                'id': booking.showroom.id,
                'name': booking.showroom.showroom_name,
                'location': booking.showroom.showroom_location,
                'regency': booking.showroom.showroom_regency,
            },
            'car': {
                'id': booking.car.id,
                'brand': booking.car.brand,
                'car_type': booking.car.car_type,
                'model': booking.car.model,
                'color': booking.car.color,
                'year': booking.car.year,
                'transmission': booking.car.transmission,
                'fuel_type': booking.car.fuel_type,
                'doors': booking.car.doors,
                'cylinder_size': booking.car.cylinder_size,
                'cylinder_total': booking.car.cylinder_total,
                'turbo': booking.car.turbo,
                'mileage': booking.car.mileage,
                'license_plate': booking.car.license_plate,
                'price_cash': booking.car.price_cash,
                'price_credit': booking.car.price_credit,
                'pkb_value': booking.car.pkb_value,
                'pkb_base': booking.car.pkb_base,
                'stnk_date': booking.car.stnk_date,
                'levy_date': booking.car.levy_date,
                'swdkllj': booking.car.swdkllj,
                'total_levy': booking.car.total_levy,
            },
            'visit_date': booking.visit_date,
            'visit_time': booking.visit_time,
            'status': booking.status,
            'notes': booking.notes,
        })
    return JsonResponse(bookings, safe=False)

@login_required(login_url='/auth/login/')
def get_bookings_by_date(request, visit_date):
    visit_date_obj = datetime.strptime(visit_date, '%b %d %Y').date()
    data = Booking.objects.select_related('user', 'showroom', 'car').filter(visit_date=visit_date_obj, user=request.user)
    bookings = []
    for booking in data:
        bookings.append({
            'id': booking.id,
            'user': {
                'id': booking.user.id,
                'username': booking.user.username,
            },
            'showroom': {
                'id': booking.showroom.id,
                'name': booking.showroom.showroom_name,
                'location': booking.showroom.showroom_location,
                'regency': booking.showroom.showroom_regency,
            },
            'car': {
                'id': booking.car.id,
                'brand': booking.car.brand,
                'car_type': booking.car.car_type,
                'model': booking.car.model,
                'color': booking.car.color,
                'year': booking.car.year,
                'transmission': booking.car.transmission,
                'fuel_type': booking.car.fuel_type,
                'doors': booking.car.doors,
                'cylinder_size': booking.car.cylinder_size,
                'cylinder_total': booking.car.cylinder_total,
                'turbo': booking.car.turbo,
                'mileage': booking.car.mileage,
                'license_plate': booking.car.license_plate,
                'price_cash': booking.car.price_cash,
                'price_credit': booking.car.price_credit,
                'pkb_value': booking.car.pkb_value,
                'pkb_base': booking.car.pkb_base,
                'stnk_date': booking.car.stnk_date,
                'levy_date': booking.car.levy_date,
                'swdkllj': booking.car.swdkllj,
                'total_levy': booking.car.total_levy,
            },
            'visit_date': booking.visit_date,
            'visit_time': booking.visit_time,
            'status': booking.status,
            'notes': booking.notes,
        })
    return JsonResponse(bookings, safe=False)

@login_required(login_url='/auth/login/')
def get_booking_by_id(request, booking_id_str):
    try:
        booking_id = uuid.UUID(booking_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)
    
    booking = get_object_or_404(Booking.objects.select_related('user', 'showroom', 'car'), id=booking_id)
    
    booking_data = {
        'id': booking.id,
        'user': {
            'id': booking.user.id,
            'username': booking.user.username,
        },
        'showroom': {
            'id': booking.showroom.id,
            'name': booking.showroom.showroom_name,
            'location': booking.showroom.showroom_location,
            'regency': booking.showroom.showroom_regency,
        },
        'car': {
            'id': booking.car.id,
            'brand': booking.car.brand,
            'car_type': booking.car.car_type,
            'model': booking.car.model,
            'color': booking.car.color,
            'year': booking.car.year,
            'transmission': booking.car.transmission,
            'fuel_type': booking.car.fuel_type,
            'doors': booking.car.doors,
            'cylinder_size': booking.car.cylinder_size,
            'cylinder_total': booking.car.cylinder_total,
            'turbo': booking.car.turbo,
            'mileage': booking.car.mileage,
            'license_plate': booking.car.license_plate,
            'price_cash': booking.car.price_cash,
            'price_credit': booking.car.price_credit,
            'pkb_value': booking.car.pkb_value,
            'pkb_base': booking.car.pkb_base,
            'stnk_date': booking.car.stnk_date,
            'levy_date': booking.car.levy_date,
            'swdkllj': booking.car.swdkllj,
            'total_levy': booking.car.total_levy,
        },
        'visit_date': booking.visit_date,
        'visit_time': booking.visit_time,
        'status': booking.status,
        'notes': booking.notes,
    }
    
    return JsonResponse(booking_data, safe=False)

def show_xml_by_id(request, id):
    data = Booking.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Booking.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
@login_required(login_url='/auth/login/')
def create_booking_ajax(request):
    showroom_id = request.POST.get("showroom_id")
    car_id = request.POST.get("car_id")
    visit_date = request.POST.get("visit_date")
    visit_time = request.POST.get("visit_time")
    notes = strip_tags(request.POST.get("notes", "")) 
    user = request.user

    try:
        showroom = ShowRoom.objects.get(id=showroom_id)
    except ShowRoom.DoesNotExist:
        return JsonResponse({"error": "Showroom not found"}, status=404)

    car = None
    if car_id:
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return JsonResponse({"error": "Car not found"}, status=404)

    try:
        visit_date = datetime.strptime(visit_date, "%Y-%m-%d").date()
        visit_time = datetime.strptime(visit_time, "%H:%M").time()
    except ValueError:
        return JsonResponse({"error": "Invalid date or time format"}, status=400)

    new_booking = Booking(
        user=user,
        showroom=showroom,
        car=car,
        visit_date=visit_date,
        visit_time=visit_time,
        notes=notes,
    )
    new_booking.save()

    return HttpResponse(b"CREATED", status=201)


from django.shortcuts import get_object_or_404
@login_required(login_url='/auth/login/')
def delete_booking(request, booking_id_str):
    try:
        booking_id = uuid.UUID(booking_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)
    
    if request.method == 'DELETE':  # Check for DELETE request
        booking = get_object_or_404(Booking, id=booking_id)
        booking.delete()
        return JsonResponse({'success': True, 'message': 'Booking deleted successfully.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

@login_required(login_url='/auth/login/')
def edit_booking(request):
    booking_id_str = request.POST.get('booking_id')
    try:
        booking_id = uuid.UUID(booking_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        showroom_id = request.POST.get("showroom_id")
        car_id = request.POST.get("car_id")
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')
        notes = request.POST.get('notes')

        errors = {}
        if not visit_date:  
            errors['visit_date'] = 'This field is required.'
        if not visit_time:
            errors['visit_time'] = 'This field is required.'
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        booking.car = Car.objects.get(id=car_id)
        booking.showroom = ShowRoom.objects.get(id=showroom_id)
        booking.visit_date = visit_date
        booking.visit_time = visit_time
        booking.notes = notes
        booking.save()

        return JsonResponse({'success': True, 'message': 'Booking updated successfully!'})

 
    return JsonResponse({'form': {
        'visit_date': booking.visit_date,
        'visit_time': booking.visit_time,
        'status': booking.status,
        'notes': booking.notes,
    }})


from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@require_POST
@login_required(login_url='/auth/login/')
@csrf_exempt
def create_booking_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        showroom_id = data.get("showroom_id")
        car_id = data.get("car_id")
        visit_date = data.get("visit_date")
        visit_time = data.get("visit_time")
        notes = strip_tags(data.get("notes", "")) 
        user = request.user

        try:
            showroom = ShowRoom.objects.get(id=showroom_id)
        except ShowRoom.DoesNotExist:
            return JsonResponse({"error": "Showroom not found"}, status=404)

        car = None
        if car_id:
            try:
                car = Car.objects.get(id=car_id)
            except Car.DoesNotExist:
                return JsonResponse({"error": "Car not found"}, status=404)

        try:
            visit_date = datetime.strptime(visit_date, "%Y-%m-%d").date()
            visit_time = datetime.strptime(visit_time, "%I:%M %p").time()
        except ValueError:
            return JsonResponse({"error": "Invalid date or time format"}, status=400)

        new_booking = Booking(
            user=user,
            showroom=showroom,
            car=car,
            visit_date=visit_date,
            visit_time=visit_time,
            notes=notes,
        )
        new_booking.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)

    
def show_booking_object(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

from django.shortcuts import get_object_or_404
@csrf_exempt
def delete_booking_flutter(request, booking_id_str):
    try:
        booking_id = uuid.UUID(booking_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)
    

    booking = get_object_or_404(Booking, id=booking_id)
    if booking != None:
        booking.delete()
        return JsonResponse({'success': True, 'message': 'Booking deleted successfully.'}, status=204)

    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)


@login_required(login_url='/auth/login/')
@csrf_exempt
def edit_booking_flutter(request):
    data = json.loads(request.body)
    booking_id_str = data.get('booking_id')
    try:
        booking_id = uuid.UUID(booking_id_str)
    except ValueError:
        return JsonResponse({'error': 'Invalid showroom ID format.'}, status=400)
    
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        showroom_id = data.get("showroom_id")
        car_id = data.get("car_id")
        visit_date = data.get('visit_date')
        visit_time = data.get('visit_time')
        visit_date = datetime.strptime(visit_date, "%Y-%m-%d").date()
        visit_time = datetime.strptime(visit_time, "%I:%M %p").time()
        notes = data.get('notes')

        errors = {}
        if not visit_date:  
            errors['visit_date'] = 'This field is required.'
        if not visit_time:
            errors['visit_time'] = 'This field is required.'
        
        if errors:
            return JsonResponse({'success': False, 'errors': errors})
        
        booking.car = Car.objects.get(id=car_id)
        booking.showroom = ShowRoom.objects.get(id=showroom_id)
        booking.visit_date = visit_date
        booking.visit_time = visit_time
        booking.notes = notes
        booking.save()

        return JsonResponse({'success': True, 'message': 'Booking updated successfully!'})

 
    return JsonResponse({'form': {
        'visit_date': booking.visit_date,
        'visit_time': booking.visit_time,
        'status': booking.status,
        'notes': booking.notes,
    }})