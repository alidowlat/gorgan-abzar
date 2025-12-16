from django.urls import path

from core import actions as views

urlpatterns = [
    path('favorites/delete', views.delete_favorite, name='delete_favorite'),
    path('favorites/delete/all', views.delete_all_favorites, name='delete_all_favorites'),
]
