from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from .models import Wishlist, Car
from django.utils.html import strip_tags

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

# Fungsi untuk menghapus item dari wishlist
@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist_view')

# Fungsi untuk menampilkan halaman wishlist
@login_required
def wishlist_view(request):
    # Mengambil semua item wishlist untuk pengguna yang sedang login
    wishlist_items = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)  # Pastikan untuk mengganti dengan template yang sesuai

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

