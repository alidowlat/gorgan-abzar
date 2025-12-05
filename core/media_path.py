import os

from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name


def get_image_upload_to(instance):
    model_name = instance.__class__.__name__.lower()
    name_part = getattr(instance, 'username', None) or getattr(instance, 'slug', None) or model_name
    slug_name = slugify(name_part)
    filename = f"{slug_name}.webp"
    return os.path.join(model_name, slug_name, filename)
