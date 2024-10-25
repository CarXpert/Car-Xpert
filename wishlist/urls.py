from django.urls import path
from .views import show_wishlist, add_note_to_wishlist_ajax, add_to_wishlist, update_note, remove_from_wishlist, add_remove_wishlist, add_or_edit_note, check_wishlist

app_name = 'wishlist' 

urlpatterns = [
    path('add_note/', add_note_to_wishlist_ajax, name='add_note_to_wishlist_ajax'),
    path('update_note/<uuid:wishlist_id>/', update_note, name='update_note'),
    path('wishlist/', show_wishlist, name='wishlist_view'),
    path('add-remove/', add_remove_wishlist, name='add_remove_wishlist'),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/', remove_from_wishlist, name='remove_from_wishlist'),
    path('add_or_edit_note/', add_or_edit_note, name='add_or_edit_note'),
    path('check-wishlist/', check_wishlist, name='check_wishlist'),

]
