from django.urls import path
from .views import show_wishlist, add_note_to_wishlist_ajax, add_to_wishlist, update_note, remove_from_wishlist

urlpatterns = [
    # path('add_note/', add_note_to_wishlist_ajax, name='add_note_to_wishlist_ajax'),
    # path('add_to_wishlist/<uuid:car_id>/', add_to_wishlist, name='add_to_wishlist'),
    # path('update_note/<uuid:wishlist_id>/', update_note, name='update_note'),
    # path('remove_from_wishlist/<uuid:wishlist_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', show_wishlist, name='wishlist_view'),
]
