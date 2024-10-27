# urls.py di app cars_detail
from django.urls import path
from . import views
from bookshowroom.views import create_booking_ajax

app_name = 'cars'

urlpatterns = [
    path('car/<uuid:car_id>/', views.car_detail, name='car_detail'),  # URL untuk detail mobilhvvhb
    path('create_booking_ajax/', create_booking_ajax, name='create_booking_ajax'),
]
