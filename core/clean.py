from core.convertors import fa_to_en_digits
from django import forms


class PhoneNumberCleanMixin(forms.Form):
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


class OTPCleanMixin(forms.Form):
    def clean_otp(self):
        otp = fa_to_en_digits(self.cleaned_data['otp'].strip())
        errors = []

        if not otp.isdigit():
            errors.append("کد تایید میبایست به صورت عددی باشد.")

        if len(otp) != 5:
            errors.append("کد تایید میبایست دقیقا ۵ رقم باشد.")

        if errors:
            raise forms.ValidationError(errors)

        return otp


def create_visit_clean(
        user,
        model,
        request,
        fk_name: str,
        http_service,
        loaded_obj
):
    ip, user_agent, referer = http_service(request)

    filter_kwargs = {
        'ip': ip,
        fk_name: loaded_obj,
    }

    if not model.objects.filter(**filter_kwargs).exists():
        model.objects.create(
            **filter_kwargs,
            user=user if user.is_authenticated else None,
            user_agent=user_agent,
            referer=referer,
        )
