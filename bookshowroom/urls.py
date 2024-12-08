from django.urls import path
from bookshowroom.views import show_booking, get_bookings, create_booking_ajax, get_showrooms, get_locations, get_cars, get_bookings_by_date
from bookshowroom.views import delete_booking, edit_booking, get_bookings_by_date, get_booking_by_id, show_booking_object
app_name = 'bookshowroom'

urlpatterns = [
    path('', show_booking, name='show_booking'),
    path('json/', get_bookings, name='show_json'),
    path('create_booking_ajax/', create_booking_ajax, name='create_booking_ajax'),
    path('get-showrooms/', get_showrooms, name='get_showrooms'),
    path('get_locations/<str:showroom_name>/', get_locations, name='get_locations'),
    path('get_cars/<str:showroom_id_str>/', get_cars, name='get_cars'),
    path('get_bookings/<str:visit_date>/', get_bookings_by_date, name='get_bookings'),
    path('delete_booking/<str:booking_id_str>/', delete_booking, name='delete_booking'),
    path('edit_booking/', edit_booking, name='edit_booking'),
    path('get_booking_by_id/<str:booking_id_str>/', get_booking_by_id, name='get_booking_by_id'),
    path('show_booking_object/', show_booking_object, name='show_booking_object')
]