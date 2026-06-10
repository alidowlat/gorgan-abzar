from django.shortcuts import render
from django.views.generic import TemplateView
from blog.models import Post
from core.actions import mark_favorites
from product.models import Product, ProductCategory, Brand
from search.models import SearchQuery
from django.db.models import Count, F
from django.db.models.functions import Lower


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        model_fields = [
            ('latest_products', Product.objects.filter(is_active=True, is_stock=True).order_by('-created_at')[:8]),
            ('featured_products', Product.objects.filter(featured=True, discount_rate__gte=2).order_by('-discount_rate')[:8]),
            ('discounted_products', Product.objects.filter(discount_rate__gte=2).order_by('-discount_rate')[:21]),
            ('categories', ProductCategory.objects.filter(is_active=True, order__gte=1, image__isnull=False).order_by('order')[:7]),
            ('brands', Brand.objects.filter(is_active=True, order__gte=1, logo__isnull=False).order_by('order')[:8]),
            ('posts', Post.objects.filter(is_active=True).annotate(visit_count=Count('visits', distinct=True)).order_by('-id')[:8]),
            ('is_home_page', True)
        ]
        for field_name, queryset in model_fields:
            context[field_name] = queryset

        mark_favorites(self.request, context['latest_products'])

        return context


def social_links(request):
    return render(
        request,
        'home/social_links.html'
    )


def site_header_component(request):
    query = request.GET.get('q', '').strip()

    results = []
    if query and len(query) >= 2:
        results = list(Product.objects.filter(title__icontains=query).values('title', 'slug', 'image')[:50])

    popular_search = (
        SearchQuery.objects
        .annotate(q=Lower('query'))
        .values(name=F('q'))
        .annotate(count=Count('id'))
        .order_by('-count')
        [:7]
    )

    categories = (
        ProductCategory.objects
        .filter(is_active=True, order__gte=1, image__isnull=False)
        .order_by('order')
        [:7]
    )

    brands = (
        Brand.objects
        .filter(is_active=True, order__gte=1, logo__isnull=False)
        .order_by('order')
        [:7]
    )

    return render(request, 'shared/header_comp.html', {
        'search_query': query,
        'search_results': results,
        'popular_search': popular_search,
        'categories': categories,
        'brands': brands,
    })


def site_footer_component(request):
    context = {}
    return render(request, 'shared/footer_comp.html', context)


def handler_404(request, exception):
    return render(request, 'home/404.html')
