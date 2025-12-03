from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'home/home.html'


def site_header_component(request):
    context = {}
    return render(request, 'shared/header_comp.html', context)


def site_footer_component(request):
    context = {}
    return render(request, 'shared/footer_comp.html', context)


def handler_404(request, exception):
    return HttpResponseNotFound('<h1>404</h1>')
