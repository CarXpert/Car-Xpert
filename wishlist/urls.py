from django.urls import path
from . import views

urlpatterns = [
    path('add_note/', views.add_note_to_wishlist_ajax, name='add_note_to_wishlist_ajax'),
    path('add_to_wishlist/<uuid:car_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('update_note/<uuid:wishlist_id>/', views.update_note, name='update_note'),
    path('remove_from_wishlist/<uuid:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
]
