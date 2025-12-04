from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from accounts.forms import PhoneForm, OTPForm
from accounts.models import User
from core.otp import set_user_otp, send_otp, is_valid_otp, OTPTooSoon


def auth_view(request):
    # delete_inactive_users(exp_in_min=15)

    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            user, created = User.objects.get_or_create(phone_number=phone_number)

            if created:
                user.set_unusable_password()
                user.save()

            try:
                otp = set_user_otp(user)
                # send_otp(user.phone_number, otp)
            except OTPTooSoon as e:
                messages.error(request, str(e))
                return redirect('verify_page')

            request.session['user_phone'] = phone_number
            return redirect('verify_page')
    else:
        form = PhoneForm()

    return render(request, 'accounts/auth.html', {'form': form})


def verify_otp_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
        # return redirect('dashboard_page')

    phone_number = request.session.get('user_phone')
    if not phone_number:
        return redirect('auth_page')

    user = User.objects.filter(phone_number=phone_number).first()
    if not user:
        return redirect('auth_page')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if is_valid_otp(user, otp):
                # is_first_verification = not user.is_verified
                # if is_first_verification:
                #     notify_user(
                #         user=user,
                #         title="تکمیل حساب کاربری",
                #         message="خوش آمدید! لطفا نسبت به تکمیل حساب کاربری خود اقدام کنید.",
                #         type_key="complete_profile",
                #         link=reverse('account_info_page')
                #     )

                user.is_verified = True
                user.save(update_fields=['is_verified'])
                login(request, user)

                user.otp = None
                user.otp_created_at = None
                user.save(update_fields=['otp', 'otp_created_at'])

                # return redirect('dashboard_page')
                return redirect('home_page')
            else:
                form.add_error('otp', 'کد وارد شده اشتباه و یا منقضی شده است.')
    else:
        form = OTPForm()

    return render(request, 'accounts/verify.html', {'form': form, 'phone_number': phone_number})


def resend_otp_view(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'invalid_method'}, status=405)

    phone = request.session.get('user_phone')
    if not phone:
        return JsonResponse({'status': 'no_phone'}, status=400)

    user = User.objects.filter(phone_number=phone).first()
    if not user:
        return JsonResponse({'status': 'not_found'}, status=404)

    if not set_user_otp(user):
        return JsonResponse({'status': 'error'}, status=500)

    send_otp(user.phone_number, user.otp)
    return JsonResponse({'status': 'ok'})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('auth_page'))
