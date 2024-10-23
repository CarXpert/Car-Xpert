from django.urls import path
from . import views

urlpatterns = [
    path('add/<uuid:car_id>/', views.add_to_wishlist, name='add'),  # Route untuk menambah ke wishlist
    path('', views.wishlist_view, name='wishlist_view'),  # View untuk melihat wishlist
    path('update_note/<int:wishlist_id>/', views.update_note, name='update_note'),  # Update notes in wishlist
    path('remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove'),  # Remove car from wishlist
]
