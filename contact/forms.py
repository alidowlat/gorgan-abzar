from django import forms
from contact.models import ContactUs

from core.convertors import fa_to_en_digits


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['name', 'phone_number', 'subject', 'message']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full p-3 outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all col-span-6 text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400',
                'placeholder': 'نام'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full p-3 outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all col-span-6 text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400',
                'dir': 'rtl',
                'name': 'phone_number',
                'placeholder': 'شماره موبایل'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'block w-full p-3 outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all col-span-6 text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400',
                'placeholder': 'عنوان'
            }),
            'message': forms.Textarea(attrs={
                'class': 'block w-full p-3 outline dark:outline-none outline-1 -outline-offset-1 placeholder:text-gray-400 transition-all col-span-6 text-gray-800 dark:text-gray-100 dark:bg-gray-900 bg-slate-100 border border-transparent hover:border-slate-200 appearance-none rounded-md outline-none focus:bg-white focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 dark:focus:ring-blue-400',
                'placeholder': 'متن پیام'
            }),
        }

        error_messages = {
            'name': {'required': 'وارد کردن نام الزامی است.'},
            'phone_number': {'required': 'وارد کردن شماره تلفن الزامی است.', 'invalid': 'شماره تلفن معتبر نیست.'},
            'subject': {'required': 'وارد کردن موضوع الزامی است.'},
            'message': {'required': 'وارد کردن پیام الزامی است.'},
        }

    def clean_phone_number(self):
        phone = fa_to_en_digits(self.cleaned_data['phone_number'].strip())
        errors = []

        if not phone.isdigit():
            errors.append("شماره موبایل نامعتبر است.")
        if not phone.startswith("09"):
            errors.append("شماره موبایل میبایست با ۰۹ شروع شود.")
        if len(phone) != 11:
            errors.append("شماره موبایل میبایست دقیقا ۱۱ رقمی باشد.")
        if errors:
            raise forms.ValidationError(errors)

        return phone
