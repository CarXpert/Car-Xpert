# urls.py di app main
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.car_list, name='car_list'),  # URL untuk menampilkan daftar mobil di main.html
]
