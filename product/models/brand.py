from django.db import models
from django.utils.text import slugify

from core.media_path import get_image_upload_to


class Brand(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default="", blank=True, unique=True, db_index=True)
    logo = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'
        db_table = 'product_brands'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)
