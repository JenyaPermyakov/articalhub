from django.urls import path
from . import views


urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('<int:pk>/edit', views.article_edit, name='article_edit'),
    path('<int:pk>/delete', views.article_delete, name='article_delete'),
]

