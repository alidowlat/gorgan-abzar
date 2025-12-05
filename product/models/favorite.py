from core.models.base_model import AbstractFavorite
from django.db import models


class Favorite(AbstractFavorite):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return f'{self.user} -> {self.product.title}'

    class Meta:
        unique_together = ('user', 'product')
        db_table = 'favorite_products'
