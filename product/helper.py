from django.db.models import Q, Count

from product.models import Product
from reviews.models import ProductReviewReaction, ProductReview


class ProductDataFetcher:
    def __init__(self, product, user=None):
        self.product = product
        self.user = user

    def get_reviews_queryset(self):
        return (
            ProductReview.objects
            .filter(product=self.product)
            .select_related('user')
        )

    def get_annotated_reviews(self):
        base_qs = self.get_reviews_queryset()

        annotated = base_qs.annotate(
            like_count=Count('reactions', filter=Q(reactions__reaction='like')),
            dislike_count=Count('reactions', filter=Q(reactions__reaction='dislike')),
        ).order_by('-created_at')

        return annotated, base_qs.count()

    def get_last_review(self):
        qs, _ = self.get_annotated_reviews()
        return qs.first()

    def get_user_reaction_ids(self):
        if not self.user or not self.user.is_authenticated:
            return [], []

        reactions = ProductReviewReaction.objects.filter(
            user=self.user,
            review__product=self.product
        ).values('review_id', 'reaction')

        liked_ids = [r['review_id'] for r in reactions if r['reaction'] == 'like']
        disliked_ids = [r['review_id'] for r in reactions if r['reaction'] == 'dislike']

        return liked_ids, disliked_ids

    def get_related_products(self):
        return (
            Product.objects
            .select_related('category', 'brand')
            .filter(
                Q(category_id=self.product.category_id) |
                Q(brand_id=self.product.brand_id)
            )
            .exclude(id=self.product.id)
            .order_by('-created_at')
            .distinct()[:8]
        )