from django.urls import path
from order import views

urlpatterns = [
    path('add-to-cart', views.add_product_to_cart, name='add_product_to_cart'),
    # path('payment-request/', views.payment_request, name='payment_request'),
    # path('payment-verify/', views.verify_payment, name='payment_verify'),
    # path('factors/', views.FactorsListView.as_view(), name='factors_list'),
    # path('factors/<int:buy_id>/', views.FactorsDetailView.as_view(), name='factors_detail'),
    # path('generate_factor_pdf/<int:order_id>/', views.generate_factor_pdf, name='generate_factor_pdf'),
]
