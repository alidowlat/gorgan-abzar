from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from core.otp import send_sms_order
from order.models import Order
from order.utils import OrderService, StockService, PaymentService
from order.utils.payment_manager import ZP_API_STARTPAY, iran_tz


@login_required
def payment_request(request):
    try:
        order = OrderService.get_unpaid_order(request.user)
        total = OrderService.calculate_total(order)
        OrderService.validate_discount(order, request.user)
        StockService.validate_order_stock(order)

        authority = PaymentService.request_payment(total, order)
        return redirect(ZP_API_STARTPAY.format(authority=authority))

    except ValueError as e:
        messages.error(request, str(e))
        return redirect('user_cart_view')


@login_required
def verify_payment(request):
    order = OrderService.get_unpaid_order(request.user)
    authority = request.GET.get("Authority")
    status_param = request.GET.get("Status")

    if not order or status_param != "OK":
        return redirect("payment_status")

    try:
        total = OrderService.calculate_total(order)
        status = PaymentService.verify_payment(authority, total)

        if status not in (100, 101):
            raise ValueError

        StockService.decrease_stock(order)

        order.is_paid = True
        order.paid_at = datetime.now(iran_tz)
        order.tracking_code = order.generate_tracking_code()
        order.status = "pending"
        order.save()

        send_sms_order(request.user.phone_number, order.tracking_code)

        return redirect("payment_status", tracking_code=order.tracking_code)

    except Exception:
        return redirect("payment_status")


@login_required
def payment_status(request, tracking_code=None):
    order = None
    if tracking_code:
        order = Order.objects.filter(
            tracking_code=tracking_code,
            user=request.user
        ).first()
    success = bool(order and order.is_paid)

    context = {
        "order": order,
        "gateway": "زرین پال",
        "order_success": success,
        "status_text": "پرداخت موفق" if success else "پرداخت ناموفق",
        "status_color": "green" if success else "red",
        "icon": "check-circle" if success else "x-circle",
    }

    if not success:
        context["error_message"] = "پرداخت لغو شده و یا نامعتبر است."

    return render(request, "order/payment/status.html", context)
