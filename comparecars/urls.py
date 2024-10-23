from django.urls import path
from . import views

urlpatterns = [
    path('compare/', views.compare_cars, name='compare_cars'),  
    path('compare/<int:id>/', views.compare_cars_with_id, name='compare_cars_with_id'),  
    path('get-cars/', views.get_cars, name='get_cars'),  
    path('list-comparisons/', views.list_comparisons, name='list_comparisons'),
]
