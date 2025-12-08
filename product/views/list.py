from django.db.models import Count
from django.views.generic import ListView

from core.actions import apply_filters
from product.models import Product, ProductCategory, Brand


class ProductListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'product/list/main.html'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        mobile_toggles = [
            {'id': 'available-toggle5', 'name': 'available', 'label': 'فقط کالا های موجود', 'value': 1,
             'checked': self.request.GET.get('available') == '1'},
            {'id': 'featured-toggle5', 'name': 'featured', 'label': 'کالا های ویژه', 'value': 1,
             'checked': self.request.GET.get('featured') == '1'},
        ]
        context['mobile_toggles'] = mobile_toggles

        desktop_toggles = [
            {'id': 'available-toggle', 'name': 'available', 'label': 'فقط کالا های موجود', 'value': 1,
             'checked': self.request.GET.get('available') == '1'},
            {'id': 'featured-toggle', 'name': 'featured', 'label': 'کالا های ویژه', 'value': 1,
             'checked': self.request.GET.get('featured') == '1'},
        ]
        context['desktop_toggles'] = desktop_toggles

        model_fields = [
            ('categories', ProductCategory.objects.filter(is_active=True)),
            ('brands', Brand.objects.filter(is_active=True)),
            ('filtered_products', apply_filters(self.request, Product.objects.all())),
        ]

        for field_name, queryset in model_fields:
            context[field_name] = queryset

        return context

    def get_queryset(self):
        qs = Product.objects.annotate(
            visit_count=Count('visits', distinct=True)
        )

        filtered_qs = apply_filters(self.request, qs)

        sort_by = self.request.GET.get('sort_by')
        match sort_by:
            case 'most_expensive':
                filtered_qs = filtered_qs.order_by('-price', '-created_at')
            case 'most_viewed':
                filtered_qs = filtered_qs.order_by('-visit_count', '-created_at')
            case 'cheapest':
                filtered_qs = filtered_qs.order_by('price', '-created_at')
            case 'newest':
                filtered_qs = filtered_qs.order_by('-created_at')

        return filtered_qs
