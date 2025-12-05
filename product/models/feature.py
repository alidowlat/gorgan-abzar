from django.db import models


class Feature(models.Model):
    product = models.ForeignKey('product.Product', related_name='features', on_delete=models.CASCADE)
    key = models.CharField(max_length=85)
    value = models.CharField(max_length=85)

    def __str__(self):
        return f"{self.product} --> {self.key}: {self.value}"
