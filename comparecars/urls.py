from django.urls import path
from . import views

urlpatterns = [
    path('compare/', views.compare_cars, name='compare_cars'),
    path('compare/<int:id>/', views.compare_cars_with_id, name='compare_cars_with_id'),
    path('compare/', views.compare_view, name='compare_view'),
]
