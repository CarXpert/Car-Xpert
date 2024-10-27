from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),  
    path('main/', views.show_main, name='show_main'),  
    path('car/<uuid:car_id>/', views.car_detail, name='car_detail'),  
    path('car/edit/<uuid:car_id>/', views.edit_car_view, name='edit_car'), 
    path('news/', include('news.urls', namespace='news')), 
    path('add_car/', views.add_car, name='add_car'),  
    path('get_cars_filtered/<str:query>/', views.get_cars_filtered, name="get_cars_filtered"),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
]
