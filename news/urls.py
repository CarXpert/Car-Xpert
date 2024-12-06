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
    path('json/', views.show_json, name='show_json'),  # Semua artikel dalam JSON
    path('xml/', views.show_xml, name='show_xml'),  # Semua artikel dalam XML
    path('<int:id>/json/', views.show_json_by_id, name='show_json_by_id'),  # Artikel berdasarkan ID dalam JSON
    path('<int:id>/xml/', views.show_xml_by_id, name='show_xml_by_id'),  # Artikel berdasarkan ID dalam XML
    path('api/add/', views.add_article_api, name='add_article_api'),
    path('api/<int:id>/edit/', views.edit_article_api, name='edit_article_api'),
    path('api/<int:id>/delete/', views.delete_article_api, name='delete_article_api'),
]
