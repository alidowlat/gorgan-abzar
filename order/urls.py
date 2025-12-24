from django.urls import path
from order import views

urlpatterns = [
    path('cart', views.UserCartView.as_view(), name='user_cart_view'),
    path('add-to-cart', views.add_product_to_cart, name='add_product_to_cart'),
    path('cart-update', views.cart_update, name='cart_update'),
    path('cart-remove', views.cart_remove, name='cart_remove'),
    path('cart-clear', views.cart_clear, name='cart_clear'),
    path('checkout', views.CheckoutView.as_view(), name='checkout_view'),
]
