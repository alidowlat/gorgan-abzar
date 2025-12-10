from django.urls import path

from contact import views

urlpatterns = [
    path('', views.contact_us, name='contact_us_page'),
]
