from django.db.models import Q, Count
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from core.actions import mark_favorites
from product.helper import ProductDataFetcher
from product.models import Product, Favorite
from reviews.models import ProductReview


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
        context = super().get_context_data(**kwargs)

        fetcher = ProductDataFetcher(self.object, self.request.user)

        reviews, reviews_count = fetcher.get_annotated_reviews()
        last_review = fetcher.get_last_review()
        liked_ids, disliked_ids = fetcher.get_user_reaction_ids()
        related_products = fetcher.get_related_products()

        context.update({
            'reviews': reviews,
            'reviews_count': reviews_count,
            'last_review': last_review,
            'liked_ids': liked_ids,
            'disliked_ids': disliked_ids,
            'related_products': related_products,
        })

        mark_favorites(self.request, context['related_products'])
        mark_favorites(self.request, context['product'])

        return context


def add_product_review(request: HttpRequest):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'ابتدا وارد حساب کاربری شوید.'}, status=401)

    product_id = request.POST.get('product_id')
    text = request.POST.get('text')
    title = request.POST.get('title')
    recommendation = request.POST.get('recommendation')

    if not product_id:
        return JsonResponse({'error': 'اطلاعات ناقص است'}, status=400)

    ProductReview.objects.create(
        user=request.user,
        product_id=product_id,
        title=title,
        text=text,
        recommendation=recommendation
    )

    reviews_qs = ProductReview.objects.filter(product_id=product_id)
    reviews_count = reviews_qs.count()

    fetcher = ProductDataFetcher(product_id, request.user)
    liked_ids, disliked_ids = fetcher.get_user_reaction_ids()

    reviews = (
        reviews_qs
        .select_related('user')
        .annotate(
            like_count=Count('reactions', filter=Q(reactions__reaction='like')),
            dislike_count=Count('reactions', filter=Q(reactions__reaction='dislike')),
        )
        .order_by('-created_at')
    )

    html = render_to_string(
        'product/detail/components/review_list.html',
        {
            'reviews': reviews,
            'liked_ids': liked_ids,
            'disliked_ids': disliked_ids,
        },
        request=request
    )
    return JsonResponse({
        'success': True,
        'html': html,
        'reviews_count': reviews_count,
    })


@require_POST
def toggle_reaction_product(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'login required'}, status=403)

    review_id = request.POST.get('review_id')
    reaction_type = request.POST.get('reaction')
    review = get_object_or_404(ProductReview, id=review_id)

    existing = review.reactions.filter(user=request.user).first()
    if existing:
        if existing.reaction == reaction_type:
            existing.delete()
        else:
            existing.reaction = reaction_type
            existing.save()
    else:
        review.reactions.create(user=request.user, reaction=reaction_type)

    like_count = review.reactions.filter(reaction='like').count()
    dislike_count = review.reactions.filter(reaction='dislike').count()

    return JsonResponse({
        'like_count': like_count,
        'dislike_count': dislike_count
    })

# @require_POST
# def toggle_favorite_product(request):
#     if not request.user.is_authenticated:
#         return JsonResponse({'success': False, 'message': 'برای انجام این عملیات باید وارد حساب شوید.'}, status=403)
#
#     service_id = request.POST.get('service_id')
#     try:
#         service = Product.objects.get(id=service_id)
#     except Product.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'service_not_found'}, status=404)
#
#     user = request.user
#     favorite, created = Favorite.objects.get_or_create(user=user, service=service)
#
#     if not created:
#         favorite.delete()
#         return JsonResponse({'status': 'removed'})
#     return JsonResponse({'status': 'added'})
