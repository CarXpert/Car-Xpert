from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from cars.models import Car  # Import Car model from app car
from .models import Wishlist  # Import Wishlist model

@login_required
def add_to_wishlist(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, car=car)
    if created:
        wishlist.save()
    return redirect('wishlist_view')  # Redirect to wishlist view after adding

@login_required
def update_note(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    if request.method == 'POST':
        wishlist_item.notes = request.POST.get('notes', '')
        wishlist_item.save()
    return redirect('wishlist_view')

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect('wishlist_view')
