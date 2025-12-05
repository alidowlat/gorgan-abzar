import io

from PIL import Image
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from core.media_path import get_image_upload_to, OverwriteStorage

MAX_SIZE = 150 * 1024


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, default="", null=False, db_index=True, blank=True, unique=True)
    image = models.ImageField(
        upload_to=get_image_upload_to,
        storage=OverwriteStorage()
    )
    price = models.PositiveIntegerField(default=0)
    discount_rate = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    guarantee = models.CharField(max_length=75, null=True, blank=True)
    description = models.TextField(max_length=800, verbose_name='توضیحات')
    category = models.ForeignKey('product.ProductCategory', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    brand = models.ForeignKey('product.Brand', on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_stock = models.BooleanField(default=False)
    stock = models.PositiveSmallIntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.image:
            return super().save(*args, **kwargs)

        super().save(*args, **kwargs)
        path = self.image.path
        img = Image.open(path).convert("RGB")

        quality = 95
        while quality > 40:
            buffer = io.BytesIO()
            img.save(buffer, format="webp", quality=quality)
            size = buffer.tell()
            if size <= MAX_SIZE:
                break
            quality -= 5

        with open(path, "wb") as f:
            f.write(buffer.getvalue())

    def get_absolute_url(self):
        # return reverse('service_detail', kwargs={'slug': self.slug})
        pass

    @property
    def final_price(self):
        if self.discount_rate > 0:
            return self.price - (self.price * self.discount_rate // 100)
        return self.price

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        db_table = 'products'
        ordering = ['-created_at']
