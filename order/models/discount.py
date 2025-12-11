from datetime import timezone
from django.core.validators import MinValueValidator
from django.db import models


class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_amount = models.PositiveIntegerField(
        validators=[MinValueValidator(1000)]
    )
    expiration_date = models.DateTimeField()

    def is_expired(self):
        return self.expiration_date < timezone.now()

    def is_valid_for_user(self, user):
        if self.is_expired():
            return False

        has_used = DiscountCodeUser.objects.filter(
            user=user,
            discount_code=self,
            is_paid=True
        ).exists()

        return not has_used and self.expiration_date >= timezone.now()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Discount Code'
        verbose_name_plural = 'Discount Codes'
        db_table = 'discount_codes'


class DiscountCodeUser(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='discount_codes')
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, related_name='users')
    used_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'discount_code')
        verbose_name = 'Discount Code User'
        verbose_name_plural = 'Discount Code Users'
        db_table = 'discount_codes_users'
