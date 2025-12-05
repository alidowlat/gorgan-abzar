from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Count
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
# from search.models import SearchQuery
from product.models import Favorite, ProductVisit


# def apply_filters(request, queryset):
#     filters = {
#         'platform__slug__in': request.GET.get('platform', '').split(','),
#         'category__slug__in': request.GET.get('category', '').split(','),
#         'profession__slug__in': request.GET.get('profession', '').split(','),
#         'locations__name_en__in': request.GET.get('location', '').split(','),
#         'tags__slug__in': request.GET.get('tag', '').split(','),
#     }
#
#     for key, value in filters.items():
#         if value and value != ['']:
#             queryset = queryset.filter(**{key: value})
#
#     if request.GET.get('available') == '1':
#         queryset = queryset.filter(is_active=True)
#
#     if request.GET.get('featured') == '1':
#         queryset = queryset.filter(is_unique=True)
#
#     search = request.GET.get('s')
#     if search:
#         queryset = queryset.filter(title__icontains=search)
#
#     return queryset


# @login_required
# def favorite_count(request):
#     count = Favorite.objects.filter(user=request.user).count()
#     return JsonResponse({'count': count})


# @require_POST
# @login_required
# def delete_favorite(request):
#     product_id = request.POST.get('product_id')
#     if product_id:
#         Favorite.objects.filter(user=request.user, product_id=product_id).delete()
#         return JsonResponse({'status': 'ok'})
#     return JsonResponse({'status': 'error', 'message': 'product_id not provided'}, status=400)
#
#
# @require_POST
# @login_required
# def delete_all_favorites(request):
#     Favorite.objects.filter(user=request.user).delete()
#     return JsonResponse({'status': 'ok'})


# @require_POST
# @login_required
# def delete_all_searches(request):
#     SearchQuery.objects.filter(user=request.user).delete()
#     return JsonResponse({'status': 'ok'})


# @login_required
# def order_items_count(request):
#     order = Order.objects.filter(user=request.user, is_paid=False).first()
#     count = order.items.count() if order else 0
#     return JsonResponse({'count': count})
