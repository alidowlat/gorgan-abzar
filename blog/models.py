import io
from PIL import Image
from django.db import models
from django.urls import reverse
from core.media_path import get_image_upload_to, OverwriteStorage
from ckeditor.fields import RichTextField

from core.models import AbstractVisit

MAX_SIZE = 400 * 1024


class Post(models.Model):
    author = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        max_length=100,
        default="",
        null=False,
        blank=True,
        db_index=True,
        unique=True
    )
    image = models.ImageField(
        upload_to=get_image_upload_to,
        storage=OverwriteStorage()
    )
    category = models.ForeignKey(
        'blog.PostCategory',
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    content = RichTextField(
        null=True
    )
    is_active = models.BooleanField(
        default=False
    )
    featured = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

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

    class Meta:
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        db_table = 'posts'


class PostCategory(models.Model):
    title = models.CharField(max_length=50)
    title_en = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, default="", blank=True, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return f"{reverse('post_list')}?category={self.slug}"

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'
        db_table = 'post_categories'


class PostVisit(AbstractVisit):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='visits')

    def __str__(self):
        return f'{self.post.title} / {self.ip}'

    class Meta:
        verbose_name = 'Post Visit'
        verbose_name_plural = 'Post Visits'
        db_table = 'posts_visits'
