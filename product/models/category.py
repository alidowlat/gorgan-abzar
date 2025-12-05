from django.db import models
from django.utils.text import slugify

from core.media_path import get_image_upload_to


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default="", blank=True, unique=True, db_index=True)
    image = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title_en)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'product_categories'
