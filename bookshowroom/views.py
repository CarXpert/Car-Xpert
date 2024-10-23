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

# @login_required(login_url='/login')
def show_booking(request):
    context = {
        'user': request.user,
        'last_login': request.COOKIES['last_login'],
    }

    return render(request, "test.html", context)

def show_xml(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Booking.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Booking.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Booking.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@require_POST
def create_booking_ajax(request):
    showroom_id = request.POST.get("showroom_id")
    car_id = request.POST.get("car_id")
    visit_date = request.POST.get("visit_date")
    visit_time = request.POST.get("visit_time")
    notes = strip_tags(request.POST.get("notes", ""))  # Strip HTML tags
    user = request.user

    # Get the related showroom and car objects
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

    # Convert visit_date and visit_time to the correct format
    try:
        visit_date = datetime.strptime(visit_date, "%Y-%m-%d").date()
        visit_time = datetime.strptime(visit_time, "%H:%M").time()
    except ValueError:
        return JsonResponse({"error": "Invalid date or time format"}, status=400)

    # Create a new booking
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

