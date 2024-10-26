from django.urls import path, include
from . import views

urlpatterns = [
    path('compare/', views.compare_cars, name='compare_cars'),  
    path('compare/<int:id>/', views.compare_cars_with_id, name='compare_cars_with_id'),  
    path('get-cars/', views.get_cars, name='get_cars'),  
    path('list-comparisons/', views.list_comparisons, name='list_comparisons'),
    # path('authentication/', include('authentication.urls')),
    path('compare/<int:id>/edit-comparison-title/', views.edit_comparison_title, name='edit_comparison_title'),
]
