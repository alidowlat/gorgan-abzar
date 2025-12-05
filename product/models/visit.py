from django.db import models

from core.models.base_model import AbstractVisit


class ProductVisit(AbstractVisit):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='visits')

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        db_table = 'product_visits'
        indexes = [
            models.Index(fields=['created_at']),
        ]
