from django.urls import path
from bookshowroom.views import show_booking
app_name = 'bookshowroom'

urlpatterns = [
    path('', show_booking, name='show_main'),
]