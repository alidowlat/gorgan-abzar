from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from accounts.models import UserAddress
from order.models import OrderItems


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/overview/main.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        model_fields = [
            (
                'latest_order_items',
                OrderItems.objects
                .filter(order__user=self.request.user)
                .select_related('order', 'product')
                .order_by('-created_at')[:3]
            ),
            (
                'user_address',
                UserAddress.objects.filter(user=self.request.user, is_default=True) if self.request.user.addresses else None
            ),
        ]
        for field_name, queryset in model_fields:
            context[field_name] = queryset

        return context
