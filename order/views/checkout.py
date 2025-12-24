from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from accounts.models import UserAddress
from order.forms import DiscountForm
from order.models import Order, DiscountCode, DiscountCodeUser
from order.utils import CartManager, OrderCalculator


class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        order, _ = Order.objects.get_or_create(user=request.user, is_paid=False)
        addresses = UserAddress.objects.filter(user=request.user)

        cart = CartManager(order)
        cart.sync_prices()
        data = cart.calculate()

        context = {
            "order": order,
            "addresses": addresses,
            "form": DiscountForm(),
            "items": data["items"],
            "total_before_discount": data["total_before_discount"],
            "total_after_discount": data["total_after_discount"],
            "discount_amount": data["discount_amount"],
            "final_price_shipping": OrderCalculator(order).total_with_shipping(),
            "full_discount": OrderCalculator(order).full_discount(),
            "total_profit": data["total_profit"],
        }
        return render(request, "order/checkout/main.html", context)

    def post(self, request):
        order = Order.objects.filter(user=request.user, is_paid=False).first()
        if not order:
            return redirect("user_cart_view")

        cart = CartManager(order)

        if "remove_discount" in request.POST:
            if order.discount_code:
                DiscountCodeUser.objects.filter(
                    user=request.user,
                    discount_code=order.discount_code
                ).delete()

                order.discount_code = None
                order.save()

            messages.success(request, "کد تخفیف حذف شد.")
            return redirect("checkout_view")

        form = DiscountForm(request.POST)
        if not form.is_valid():
            messages.error(request, "کد تخفیف نامعتبر و یا منقضی شده است.")
            return redirect("checkout_view")

        if order.discount_code:
            messages.error(request, "کد تخفیف قبلاً اعمال شده است.")
            return redirect("checkout_view")

        success, message = cart.apply_discount_code(
            user=request.user,
            code=form.cleaned_data["discount_code"]
        )
        messages.success(request, message) if success else messages.error(request, message)

        return redirect("checkout_view")
