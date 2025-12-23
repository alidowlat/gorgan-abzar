from collections.abc import Iterable

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from accounts.models import UserAddress
# from search.models import SearchQuery
from product.models import Favorite, ProductVisit


def apply_filters(request, queryset):
    filters = {
        'brand__slug__in': request.GET.get('brand', '').split(','),
        'category__slug__in': request.GET.get('category', '').split(','),
    }

    for key, value in filters.items():
        if value and value != ['']:
            queryset = queryset.filter(**{key: value})

    if request.GET.get('available') == '1':
        queryset = queryset.filter(is_stock=True)

    if request.GET.get('featured') == '1':
        queryset = queryset.filter(featured=True)

    return queryset


def apply_filters_blog(request, queryset):
    filters = {
        'category__slug__in': request.GET.get('category', '').split(','),
    }

    for key, value in filters.items():
        if value and value != ['']:
            queryset = queryset.filter(**{key: value})

    if request.GET.get('available') == '1':
        queryset = queryset.filter(is_stock=True)

    if request.GET.get('featured') == '1':
        queryset = queryset.filter(featured=True)

    return queryset


def mark_favorites(request, products):
    if request.user.is_authenticated:
        favorite_ids = set(
            Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
        )
    else:
        favorite_ids = set()

    if not isinstance(products, Iterable):
        products = [products]

    for product in products:
        product.is_favorited = product.id in favorite_ids

@require_POST
@login_required
def delete_favorite(request):
    product_id = request.POST.get('product_id')
    if product_id:
        Favorite.objects.filter(user=request.user, product_id=product_id).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'product_id not provided'}, status=400)


@require_POST
@login_required
def delete_all_favorites(request):
    Favorite.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'ok'})


@require_POST
@login_required
def delete_address(request):
    address_id = request.POST.get('address_id')
    if address_id:
        UserAddress.objects.filter(user=request.user, id=address_id).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error', 'message': 'address_id not provided'}, status=400)

# @require_POST
# @login_required
# def delete_all_searches(request):
#     SearchQuery.objects.filter(user=request.user).delete()
#     return JsonResponse({'status': 'ok'})
#
#
# @login_required
# def order_items_count(request):
#     order = Order.objects.filter(user=request.user, is_paid=False).first()
#     count = order.items.count() if order else 0
#     return JsonResponse({'count': count})
