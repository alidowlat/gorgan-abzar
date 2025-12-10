from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView

from core.actions import mark_favorites
from product.models import Product, ProductCategory, Brand


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        model_fields = [
            ('latest_products', Product.objects.all().order_by('-created_at')[:8]),
            ('discounted_products', Product.objects.filter(discount_rate__gte=2).order_by('-discount_rate')[:8]),
            ('categories', ProductCategory.objects.filter(is_active=True).order_by('-id')[:8]),
            ('brands', Brand.objects.filter(is_active=True).order_by('-id')[:8]),
        ]
        for field_name, queryset in model_fields:
            context[field_name] = queryset

        mark_favorites(self.request, context['latest_products'])

        return context


def site_header_component(request):
    context = {}
    return render(request, 'shared/header_comp.html', context)


def site_footer_component(request):
    context = {}
    return render(request, 'shared/footer_comp.html', context)


def handler_404(request, exception):
    return HttpResponseNotFound('<h1>404</h1>')
