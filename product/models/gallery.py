from django.db import models

from core.media_path import get_image_upload_to, OverwriteStorage


class Gallery(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_upload_to, storage=OverwriteStorage())

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        db_table = 'product_galleries'
