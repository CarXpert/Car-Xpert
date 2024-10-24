# news/urls.py
from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_article_list, name='news_article_list'),  # Root of /news/ will show news articles
    path('add/', views.create_article, name='create_article'),     # /news/add/
    path('<int:id>/edit/', views.edit_article, name='edit_article'),  # /news/<id>/edit/
    path('<int:id>/delete/', views.delete_article, name='delete_article'),  # /news/<id>/delete/
]
