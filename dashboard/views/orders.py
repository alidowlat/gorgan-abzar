from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from order.models import Order, OrderItems


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


class OrderItemListView(LoginRequiredMixin, ListView):
    model = OrderItems
    template_name = "dashboard/order/item/main.html"
    context_object_name = "items"

    def get_queryset(self):
        self.order = get_object_or_404(
            Order,
            id=self.kwargs["order_id"],
            user=self.request.user,
            is_paid=True
        )
        return (
            OrderItems.objects
            .filter(order=self.order)
            .select_related("product")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        return context