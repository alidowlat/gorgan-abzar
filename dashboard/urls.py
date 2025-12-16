from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_view'),
    path('orders', views.OrderListView.as_view(), name='orders_view'),
    path('orders/<int:order_id>/items', views.OrderItemListView.as_view(), name='order_items_view'),
    path('favorites', views.FavoriteProductsView.as_view(), name='favorite_products_view'),
    path('address', views.AddressListView.as_view(), name='address_list_view'),
    path('address/create', views.AddressCreateView.as_view(), name='address_create_view'),
    path('address/<int:pk>/edit/', views.AddressUpdateView.as_view(), name='address_update_view'),
    path('address/set-default/<int:pk>/', views.set_default_address, name='set_default_address'),
]
