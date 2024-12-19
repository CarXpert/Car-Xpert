from django.urls import path
from . import views

app_name = 'authentication'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),  
    path('login_django/', views.login_django, name='login_django'),
    path('register_django/', views.register_django, name='register_django'),
    path('logout_django/', views.logout_django, name='logout_django'),
]
