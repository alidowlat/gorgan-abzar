from django.urls import path
from product.views import ProductDetailView, ProductListView, add_product_review, toggle_reaction_product

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-review', add_product_review, name='add_product_review'),
    path('toggle-reaction', toggle_reaction_product, name='toggle_reaction_product'),
    # path('toggle-favorite', toggle_favorite_product, name='toggle_favorite_product'),
]
