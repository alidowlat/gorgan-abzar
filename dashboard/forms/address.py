from django import forms
from accounts.models import UserAddress


class AddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'full_name',
            'phone_number',
            'state',
            'city',
            'postal_code',
            'plaque',
            'full_address',
            'is_default'
        ]
        widgets = {
            'full_address': forms.Textarea(attrs={'rows': 3})
        }
