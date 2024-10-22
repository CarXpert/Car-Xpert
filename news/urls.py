from django.urls import path
from . import views

urlpatterns = [
    path('news/', views.news_article_list, name='news_article_list'),
    path('news/add/', views.create_article, name='create_article'),
    path('news/<int:id>/edit/', views.edit_article, name='edit_article'),
    path('news/<int:id>/delete/', views.delete_article, name='delete_article'),
]
