
# urls.py di app main
from django.urls import path
from main.views import show_main, car_detail

app_name = 'main'

urlpatterns = [
    path ('',show_main, name='show_main'),
    path('car/<uuid:car_id>/', car_detail, name='car_detail'), 
    # path('/car',car_list, name='car_list'),  # URL untuk menampilkan daftar mobil di main.html
]