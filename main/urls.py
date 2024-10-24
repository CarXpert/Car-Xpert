# urls.py di app main
from django.urls import path,include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.show_main, name='show_main'),  # URL untuk halaman utama (daftar mobil)
    path('car/<uuid:car_id>/', views.car_detail, name='car_detail'),  # Detail mobil
    path('news/', include('news.urls', namespace='news')),
    
]
