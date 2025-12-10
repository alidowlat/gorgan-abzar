from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(regex=r'^09\d{9}$', message="لطفا شماره موبایل خود را به درستی وارد کنید.")


class ContactUs(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=40)
    phone_number = models.CharField(validators=[phone_regex], max_length=11, blank=False, null=False)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"{self.user.get_full_name()} - {self.subject}"
        elif self.name:
            return f"{self.name} - {self.subject}"
        else:
            return f"{self.phone_number} - {self.subject}"

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'
        db_table = 'contact'
