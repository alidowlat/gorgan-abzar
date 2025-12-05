from django.urls import path

from product.views.list import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
]