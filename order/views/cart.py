from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from order.models import Order
from order.utils.cart_manager import CartManager


class UserCartView(LoginRequiredMixin, View):
    def get(self, request):
        order, _ = Order.objects.get_or_create(user=request.user, is_paid=False)

        cart = CartManager(order)
        cart.sync_prices()
        data = cart.calculate()

        context = {
            "order": order,
            "items": data["items"],
            "total_before_discount": data["total_before_discount"],
            "total_after_discount": data["total_after_discount"],
            "discount_amount": data["discount_amount"],
            "final_price": data["final_price"],
            "total_profit": data["total_profit"],
        }
        return render(request, "order/cart/main.html", context)
