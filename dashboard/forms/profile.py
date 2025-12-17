import re
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        error_messages={'required': 'وارد کردن نام الزامی است.'}
    )
    last_name = forms.CharField(
        required=True,
        error_messages={'required': 'وارد کردن نام خانوادگی الزامی است.'}
    )
    email = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not email:
            return email

        if re.search(r'[آ-ی]', email):
            raise ValidationError('ایمیل نباید شامل حروف فارسی باشد')

        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            raise ValidationError('فرمت ایمیل نامعتبر است.')

        return email

    def clean_first_name(self):
        value = self.cleaned_data.get('first_name', '').strip()
        if not value:
            raise forms.ValidationError('وارد کردن نام الزامی است')
        return value

    def clean_last_name(self):
        value = self.cleaned_data.get('last_name', '').strip()
        if not value:
            raise forms.ValidationError('وارد کردن نام خانوادگی الزامی است')
        return value

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save(update_fields=['first_name', 'last_name', 'email'])
        return user
