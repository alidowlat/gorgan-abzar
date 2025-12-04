from django.urls import path
from accounts import views

urlpatterns = [
    path('', views.auth_view, name='auth_page'),
    path('verify/', views.verify_otp_view, name='verify_page'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
