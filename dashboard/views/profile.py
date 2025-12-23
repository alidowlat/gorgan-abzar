from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, UpdateView
from accounts.forms import PhoneForm, OTPForm
from core.otp import set_user_otp, OTPTooSoon, is_valid_otp, send_otp
from dashboard.forms.profile import ProfileUpdateForm


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = 'dashboard/profile/main.html'

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = 'dashboard/profile/update/main.html'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'اطلاعات حساب کاربری با موفقیت بروزرسانی شد'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)


@login_required
def change_phone_view(request):
    user = request.user

    if request.method == 'POST':
        form = PhoneForm(request.POST)
        if form.is_valid():
            new_phone = form.cleaned_data['phone_number']

            if new_phone == user.phone_number:
                form.add_error('phone_number', 'شماره جدید نمی‌تواند مشابه شماره فعلی باشد.')
                return render(request, 'dashboard/profile/update/change-phone.html', {
                    'form': form
                })

            if User.objects.filter(phone_number=new_phone).exists():
                form.add_error('phone_number', 'این شماره قبلاً توسط کاربر دیگری ثبت شده است.')
                return render(request, 'dashboard/profile/update/change-phone.html', {
                    'form': form
                })

            try:
                set_user_otp(user)
            except OTPTooSoon as e:
                messages.error(request, str(e))
                return redirect('change_phone_verify')

            request.session['new_phone'] = new_phone
            return redirect('change_phone_verify')
    else:
        form = PhoneForm()

    return render(request, 'dashboard/profile/update/change-phone.html', {
        'form': form
    })


@login_required
def change_phone_verify_view(request):
    phone_number = request.session.get('new_phone')
    if not phone_number:
        return redirect('change_phone')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if is_valid_otp(request.user, otp):
                request.user.phone_number = phone_number
                request.user.otp = None
                request.user.otp_created_at = None
                request.user.save(update_fields=['phone_number', 'otp', 'otp_created_at'])

                del request.session['new_phone']
                return redirect('profile_view')
            else:
                form.add_error('otp', 'کد وارد شده اشتباه و یا منقضی شده است')
    else:
        form = OTPForm()

    return render(request, 'dashboard/profile/update/verify-phone.html', {
        'form': form,
        'phone_number': phone_number
    })


@login_required
@require_POST
def resend_change_phone_otp(request):
    phone = request.session.get('new_phone')
    if not phone:
        return JsonResponse({'status': 'no_phone'}, status=400)

    set_user_otp(request.user)
    # send_otp(phone, request.user.otp)
    return JsonResponse({'status': 'ok'})

