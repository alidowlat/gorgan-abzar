from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import DetailView, UpdateView

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
