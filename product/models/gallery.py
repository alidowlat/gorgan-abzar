import io
from PIL import Image
from django.db import models
from core.media_path import get_gallery_upload_to, OverwriteStorage

MAX_SIZE = 150 * 1024


class Gallery(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE, related_name='galleries')
    image = models.ImageField(upload_to=get_gallery_upload_to, storage=OverwriteStorage(), null=False, blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path).convert("RGB")
        quality = 95
        while quality > 40:
            buffer = io.BytesIO()
            img.save(buffer, format="webp", quality=quality)
            if buffer.tell() <= MAX_SIZE:
                break
            quality -= 5
        with open(self.image.path, "wb") as f:
            f.write(buffer.getvalue())

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        db_table = 'product_galleries'
