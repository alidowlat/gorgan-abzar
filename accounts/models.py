from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from accounts.managers import UserManager

phone_regex = RegexValidator(regex=r'^09\d{9}$', message="لطفا شماره موبایل خود را به درستی وارد کنید.")
otp_regex = RegexValidator(regex=r'^\d{5}$', message='کد تایید باید دقیقا ۵ رقم عددی باشد.')
postal_code_regex = RegexValidator(r'^[0-9]{10}$', 'کد پستی شما باید دقیقاً 10 رقم باشد.')


class User(AbstractUser):
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    first_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=40,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        unique=True,
        max_length=11,
        blank=False,
        null=False,
    )
    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )
    otp = models.CharField(
        max_length=5,
        validators=[otp_regex],
        null=True,
        blank=True,
    )
    otp_created_at = models.DateTimeField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def get_full_name(self):
        return f"{(self.first_name or '').strip()} {(self.last_name or '').strip()}".strip()

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return full_name
        return self.email or self.phone_number or "Unknown User"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'


class UserAddress(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='addresses',
    )
    full_name = models.CharField(
        max_length=55
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=11,
    )
    state = models.CharField(
        max_length=255,
    )
    city = models.CharField(
        max_length=255,
    )
    postal_code = models.CharField(
        max_length=10,
        validators=[postal_code_regex]
    )
    plaque = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    full_address = models.TextField()
    is_default = models.BooleanField(
        default=False,
        db_index=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user} - {self.state} - {self.city}"

    def save(self, *args, **kwargs):
        if self.is_default:
            UserAddress.objects.filter(
                user=self.user,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Address'
        verbose_name_plural = 'Address List'
        db_table = 'addresses'
