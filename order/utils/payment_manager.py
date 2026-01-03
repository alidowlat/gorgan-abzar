import pytz
import requests
from decouple import config
from order.models import Order, DiscountCodeUser

MERCHANT = config('ZP_API')
ZP_API_REQUEST = config('ZP_API_REQUEST')
ZP_API_VERIFY = config('ZP_API_VERIFY')
ZP_API_STARTPAY = config('ZP_API_STARTPAY')
CallbackURL = config('ZP_API_CALLBACKURL')
amount = 1000
description = "خرید خود را نهایی کنید !"
iran_tz = pytz.timezone('Asia/Tehran')


class OrderService:
    @staticmethod
    def get_unpaid_order(user):
        return Order.objects.get(is_paid=False, user=user)

    @staticmethod
    def calculate_total(order):
        total = order.get_final_price()
        if total <= 0:
            raise ValueError("invalid_order_total")
        return total

    @staticmethod
    def validate_discount(order, user):
        if not order.discount_code:
            return
        if DiscountCodeUser.objects.filter(
                is_paid=True,
                discount_code=order.discount_code,
                user=user
        ).exists():
            raise ValueError("discount_used")


class StockService:
    @staticmethod
    def validate_order_stock(order):
        for item in order.items.all():
            if item.product.stock < item.count:
                raise ValueError(
                    f"insufficient_stock:{item.product.title}"
                )

    @staticmethod
    def decrease_stock(order):
        for item in order.items.all():
            product = item.product
            if product.stock < item.count:
                raise ValueError("stock_conflict")

            product.stock -= item.count
            if product.stock == 0:
                product.is_stock = False
                product.is_active = False
            product.save()


class PaymentService:
    @staticmethod
    def request_payment(amount, order):
        buyer_number = f"{order.user.phone_number}"
        total_items = sum(item.count for item in order.items.all())

        description = f"{buyer_number} - {total_items} Product(s)"
        print(description)
        data = {
            "merchant_id": MERCHANT,
            "amount": int(amount * 10),
            "callback_url": CallbackURL,
            "description": description,
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        res = requests.post(ZP_API_REQUEST, json=data, headers=headers).json()

        if res.get("errors"):
            print(res.get("errors"))
            raise ValueError("payment_request_failed")

        return res["data"]["authority"]

    @staticmethod
    def verify_payment(authority, amount):
        data = {
            "merchant_id": MERCHANT,
            "amount": int(amount * 10),
            "authority": authority
        }
        headers = {"accept": "application/json", "content-type": "application/json"}
        res = requests.post(ZP_API_VERIFY, json=data, headers=headers).json()

        if res.get("errors"):
            raise ValueError("payment_verify_failed")

        return res["data"]["code"]
