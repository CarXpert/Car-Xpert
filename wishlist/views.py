import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Wishlist, Car
from wishlist.forms import WishlistNoteForm
from django.core import serializers

@login_required(login_url='/auth/login/')
def show_wishlist(request):
    sort_order = request.GET.get('sort', 'newest')
    wishlist_items = Wishlist.objects.filter(user=request.user)
    
    if sort_order == 'newest':
        wishlist_items = wishlist_items.order_by('-created_at')
    else:
        wishlist_items = wishlist_items.order_by('created_at')

    car_ids = wishlist_items.values_list('car', flat=True)
    car_objects = Car.objects.filter(id__in=car_ids)

    wishlist_with_cars = []
    for item in wishlist_items:
        car = item.car
        wishlist_with_cars.append({
            'wishlist_item': item,
            'car': car
        })

    context = {
        'wishlist_items': wishlist_with_cars,  
        'sort_order': sort_order,
    }

    return render(request, 'wishlist/wishlist_page.html', context)

@csrf_exempt
def add_remove_wishlist(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        user = request.user
        try:
            car = Car.objects.get(id=car_id)
            wishlist_item, created = Wishlist.objects.get_or_create(user=user, car=car)
            if created:
                in_wishlist = True
            else:
                wishlist_item.delete()
                in_wishlist = False
            return JsonResponse({'in_wishlist': in_wishlist, 'message': 'Wishlist updated successfully.'})
        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def remove_from_wishlist(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        user = request.user
        try:
            wishlist_item = Wishlist.objects.get(user=user, car__id=car_id)
            wishlist_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Item removed from wishlist.'}, status=200)
        except Wishlist.DoesNotExist:
            return JsonResponse({'status': 'not found', 'message': 'Item not found in wishlist.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'bad request', 'message': 'Invalid request method.'}, status=400)

def get_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    return JsonResponse({'wishlist': list(wishlist_items.values())})

def check_wishlist(request):
    car_id = request.GET.get('car_id')
    car = get_object_or_404(Car, id=car_id)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, car=car)
        in_wishlist = True
        note = wishlist_item.notes  
    except Wishlist.DoesNotExist:
        in_wishlist = False
        note = None  

    return JsonResponse({
        'in_wishlist': in_wishlist,
        'note': note  
    })

@csrf_exempt
def edit_note(request, pk):
    wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WishlistNoteForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success', 'message': 'Note updated successfully.'}, status=200)
            return redirect('wishlist:wishlist_view')  
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Form validation failed.', 'errors': form.errors}, status=400)
    else:
        form = WishlistNoteForm(instance=wishlist_item)
    return render(request, 'wishlist/edit_note.html', {'form': form, 'wishlist_item': wishlist_item})

def show_json(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('car__showroom')
    data = []
    for item in wishlist_items:
        data.append({
            'pk': item.pk,
            'car': {
                'carId': item.car.pk,
                'brand': item.car.brand,
                'car_type': item.car.car_type.capitalize(),
                'showroom': item.car.showroom.showroom_name.capitalize()  
            },
            'notes': item.notes,
            'created_at': item.created_at.isoformat(),
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def edit_note_api(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        new_note = request.POST.get('note', '')
        user = request.user
        try:
            wishlist_item = Wishlist.objects.get(user=user, car__id=car_id)
            wishlist_item.notes = new_note
            wishlist_item.save()
            return JsonResponse({'status': 'success', 'message': 'Note updated successfully.'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'bad request', 'message': 'Invalid request method.'}, status=400)