# urls.py di app cars_detail
from django.urls import path
from . import views

app_name = 'cars_detail'

urlpatterns = [
    path('car/<uuid:car_id>/', views.car_detail, name='car_detail'),  # URL untuk detail mobil
]
