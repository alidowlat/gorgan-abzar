from django.urls import path

from core import actions as views

urlpatterns = [
    # ---FAVORITE---
    path('favorites/delete', views.delete_favorite, name='delete_favorite'),
    path('favorites/delete/all', views.delete_all_favorites, name='delete_all_favorites'),

    # ---ADDRESS---
    path('address/delete', views.delete_address, name='delete_address'),
]
