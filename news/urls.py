# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_article_list, name='news_article_list'),  # Root of /news/ will show news articles
    path('add/', views.create_article, name='create_article'),     # /news/add/
    path('<int:id>/edit/', views.edit_article, name='edit_article'),  # /news/<id>/edit/
    path('<int:id>/delete-direct/', views.delete_article_direct, name='delete_article_direct'),
    path('<int:id>/', views.news_detail, name='news_detail'),
]
