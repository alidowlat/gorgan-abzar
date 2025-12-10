from django.db import models


class Settings(models.Model):
    name = models.CharField(max_length=35)
    logo_1 = models.ImageField(upload_to='setting_logo/logo_1', null=True, blank=True)
    logo_2 = models.ImageField(upload_to='setting_logo/logo_2', null=True, blank=True)
    transparent_logo = models.ImageField(upload_to='site_setting/transparent_logo', null=True, blank=True)
    footer_text = models.TextField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    is_main = models.BooleanField(default=False, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Website Setting'
        verbose_name_plural = "Website Settings"
        db_table = 'website_settings'

    def __str__(self):
        return self.name
