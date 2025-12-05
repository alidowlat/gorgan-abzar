from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView

from product.models import Product


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list/main.html'
    paginate_by = 3

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_stock=True).order_by('-created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        return context

    # def get_queryset(self):
    #     base_qs = Product.objects.annotate(
    #         visit_count=Count('visits', distinct=True),
    #     )
    #
    #     filtered_qs = apply_filters(self.request, base_qs)
    #
    #     sort_by = self.request.GET.get('sort_by')
    #     match sort_by:
    #         case 'most_expensive':
    #             filtered_qs = filtered_qs.order_by('-max_price', '-id')
    #         case 'most_viewed':
    #             filtered_qs = filtered_qs.order_by('-visit_count', '-id')
    #         case 'cheapest':
    #             filtered_qs = filtered_qs.order_by('min_price', '-id')
    #         case 'newest':
    #             filtered_qs = filtered_qs.order_by('-id')
    #
    #     return filtered_qs
