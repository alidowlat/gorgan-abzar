from django.db import models

from core.models import AbstractReview, AbstractReviewReaction


class ProductReview(AbstractReview):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'Product Review'
        verbose_name_plural = 'Product Reviews'
        db_table = 'product_reviews'


class ProductReviewReaction(AbstractReviewReaction):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, related_name='reactions')

    class Meta:
        unique_together = ('user', 'review')
        verbose_name = 'Product Review Reaction'
        verbose_name_plural = 'Product Review Reactions'
        db_table = 'product_review_reactions'

    def __str__(self):
        return f"{self.reaction} - {self.review}"
