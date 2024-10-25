from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import Wishlist, Car
from django.utils.html import strip_tags

from django.shortcuts import render
from django.db.models import Min, Max
from .models import Wishlist  # Adjust import according to your app structure
from cars.models import Car  # Import Car model

@login_required
def show_wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    wishlist_ids = wishlist_items.values_list('car_id', flat=True)
    context = {
        'wishlist_items': wishlist_items,
        'wishlist_ids': wishlist_ids, 
    }
    return render(request, 'wishlist/wishlist_page.html', context)


# Fungsi untuk menambahkan atau memperbarui catatan pada wishlist melalui AJAX
@csrf_exempt
@require_POST
def add_note_to_wishlist_ajax(request):
    car_id = request.POST.get("car_id")
    note = strip_tags(request.POST.get("note"))  # Menghapus tag HTML dari catatan
    user = request.user  # Mengambil user yang login

    # Ambil objek mobil berdasarkan car_id
    car = get_object_or_404(Car, id=car_id)

    # Periksa apakah item wishlist sudah ada, jika tidak, buat yang baru
    wishlist_item, created = Wishlist.objects.get_or_create(user=user, car=car)

    # Tambahkan atau perbarui catatan
    wishlist_item.note = note
    wishlist_item.save()

    return JsonResponse({'message': 'Catatan berhasil diperbarui!'}, status=200)

# Fungsi untuk menambahkan mobil ke wishlist
@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, car=car)
    if created:
        wishlist.save()
    return redirect('wishlist_view')  # Redirect to wishlist view after adding

# Fungsi untuk memperbarui catatan dalam wishlist
@login_required
def update_note(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    if request.method == 'POST':
        note = request.POST.get('note', '')
        wishlist_item.note = note
        wishlist_item.save()
    return redirect('wishlist_view')

@login_required
def car_list_view(request):
    cars = Car.objects.all()  # Ambil semua mobil

    # Filter berdasarkan harga
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min and price_max:
        cars = cars.filter(price_cash__gte=price_min, price_cash__lte=price_max)

    # Filter berdasarkan tahun
    year_min = request.GET.get('year_min')
    year_max = request.GET.get('year_max')
    if year_min and year_max:
        cars = cars.filter(year__gte=year_min, year__lte=year_max)

    context = {
        'cars': cars,
    }
    return render(request, 'car_list.html', context)  # Ganti dengan template yang sesuai

@login_required
def add_remove_wishlist(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        user = request.user

        try:
            # Ambil mobil dari database
            car = Car.objects.get(id=car_id)

            # Buat atau hapus wishlist item
            wishlist_item, created = Wishlist.objects.get_or_create(user=user, car=car)

            # Periksa apakah item baru dibuat atau dihapus
            if created:
                in_wishlist = True  # Mobil ditambahkan ke wishlist
            else:
                wishlist_item.delete()
                in_wishlist = False  # Mobil dihapus dari wishlist

            # Berikan respons JSON
            return JsonResponse({
                'in_wishlist': in_wishlist,
                'message': 'Wishlist updated successfully.'
            })

        except Car.DoesNotExist:
            return JsonResponse({'error': 'Car not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def remove_from_wishlist(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        user = request.user
        
        try:
            # Ambil item wishlist untuk mobil dan pengguna yang ditentukan
            wishlist_item = Wishlist.objects.get(user=user, car__id=car_id)
            wishlist_item.delete()  # Hapus item dari wishlist
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

@require_POST
def add_or_edit_note(request):
    car_id = request.POST.get('car_id')
    note = request.POST.get('note')
    
    wishlist_item = Wishlist.objects.get(car__id=car_id, user=request.user)
    wishlist_item.note = note
    wishlist_item.save()
    
    return JsonResponse({'success': True})

def check_wishlist(request):
    car_id = request.GET.get('car_id')
    car = get_object_or_404(Car, id=car_id)
    in_wishlist = Wishlist.objects.filter(user=request.user, car=car).exists()
    return JsonResponse({'in_wishlist': in_wishlist})
