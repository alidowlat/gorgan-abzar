from django.urls import path
from home import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('social-links/', views.social_links, name='social_links'),
]
