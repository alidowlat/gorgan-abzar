from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from order.models import Order


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "dashboard/order/main.html"
    context_object_name = "orders"
    paginate_by = 10

    def get_queryset(self):
        return (
            Order.objects
            .filter(user=self.request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )
