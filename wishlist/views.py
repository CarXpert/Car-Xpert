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
        wishlist_items = Wishlist.objects.filter(user=request.user).order_by('-created_at')
    else:
        wishlist_items = Wishlist.objects.filter(user=request.user).order_by('created_at')
    context = {
        'wishlist_items': wishlist_items,
        'sort_order': sort_order,
    }
    return render(request, 'wishlist/wishlist_page.html', context)

@login_required(login_url='/auth/login/')
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

@login_required(login_url='/auth/login/')
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

from wishlist.forms import WishlistNoteForm

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

@login_required(login_url='/auth/login/')
def edit_note(request, pk):
    wishlist_item = get_object_or_404(Wishlist, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = WishlistNoteForm(request.POST, instance=wishlist_item)
        if form.is_valid():
            form.save() 
            return redirect('wishlist:wishlist_view')  
    else:
        form = WishlistNoteForm(instance=wishlist_item)  
    
    return render(request, 'wishlist/edit_note.html', {'form': form, 'wishlist_item': wishlist_item})

def show_json(request):
    data = Wishlist.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")