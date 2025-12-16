from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard_view'),
    path('orders', views.OrderListView.as_view(), name='orders_view'),
    path('orders/<int:order_id>/items', views.OrderItemListView.as_view(), name='order_items_view'),
]
