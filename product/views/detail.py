from django.db.models import Q
from django.views.generic import DetailView

from product.models import Product


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'product/detail/main.html'

    def get_queryset(self):
        return (
            Product.objects
            .select_related('category', 'brand')
            .prefetch_related('galleries', 'features')
        )

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        latest_products = (
            Product.objects
            .select_related('category', 'brand')
            .filter(
                Q(category_id=self.object.category_id) |
                Q(brand_id=self.object.brand_id)
            )
            .exclude(id=self.object.id)
            .order_by('-created_at')
            .distinct()[:8]
        )
        context['latest_products'] = latest_products

        return context
