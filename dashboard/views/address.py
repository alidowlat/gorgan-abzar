from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView
from accounts.models import UserAddress
from dashboard.forms import AddressForm


class AddressListView(LoginRequiredMixin, ListView):
    model = UserAddress
    template_name = 'dashboard/address/main.html'
    context_object_name = 'address_list'

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class AddressCreateView(LoginRequiredMixin, CreateView):
    model = UserAddress
    form_class = AddressForm
    template_name = 'dashboard/address/create/form.html'

    def form_valid(self, form):
        address = form.save(commit=False)
        address.user = self.request.user

        if address.is_default:
            UserAddress.objects.filter(
                user=self.request.user,
                is_default=True
            ).update(is_default=False)

        address.save()

        return JsonResponse({
            'status': 'success',
            'message': 'آدرس شما با موفقیت ثبت شد'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = UserAddress
    context_object_name = 'address'
    form_class = AddressForm
    template_name = 'dashboard/address/edit/form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            UserAddress,
            id=self.kwargs['pk'],
            user=self.request.user
        )

    def form_valid(self, form):
        address = form.save(commit=False)

        if address.is_default:
            UserAddress.objects.filter(
                user=self.request.user,
                is_default=True
            ).exclude(id=address.id).update(is_default=False)

        address.save()

        return JsonResponse({
            'status': 'success',
            'message': 'آدرس شما با موفقیت ویرایش شد'
        })

    def form_invalid(self, form):
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        }, status=400)


@login_required
def set_default_address(request, pk):
    if request.method == "POST":
        try:
            address = UserAddress.objects.get(pk=pk, user=request.user)
        except UserAddress.DoesNotExist:
            return JsonResponse({"status": "error", "message": "آدرس یافت نشد"}, status=404)

        # غیر فعال کردن سایر آدرس‌ها
        UserAddress.objects.filter(user=request.user, is_default=True).update(is_default=False)

        # فعال کردن این آدرس
        address.is_default = True
        address.save()

        return JsonResponse({"status": "success", "message": "آدرس پیش‌فرض تغییر کرد"})
    return JsonResponse({"status": "error", "message": "درخواست نامعتبر"}, status=400)
