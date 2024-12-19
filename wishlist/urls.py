from django.urls import path
from .views import show_wishlist, add_remove_wishlist, remove_from_wishlist, check_wishlist, edit_note, show_json, edit_note_api

app_name = 'wishlist' 

urlpatterns = [
    path('wishlist/', show_wishlist, name='wishlist_view'),
    path('add-remove/', add_remove_wishlist, name='add_remove_wishlist'),
    path('remove/', remove_from_wishlist, name='remove_from_wishlist'),
    path('check-wishlist/', check_wishlist, name='check_wishlist'),
    path('edit-note/<int:pk>/', edit_note, name='edit_note'),  
    path('json/', show_json, name='show_json'),
    path('edit-note-api/', edit_note_api, name='edit_note_api'),

]
