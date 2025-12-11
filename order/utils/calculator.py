import secrets


class OrderCalculator:
    def __init__(self, order):
        self.order = order
        self.items = order.items.all()

    # قیمت آیتم قبل از پرداخت (قیمت محصول → اگر تخفیف محصول داشت اعمال میشود)
    def item_live_price(self, item):
        return item.product.final_price

    # قیمت آیتم پس از پرداخت (قیمت فریز شده)
    def item_frozen_price(self, item):
        return item.final_price

    # مجموع قیمت آیتم‌ها
    def items_total(self):
        total = 0
        for item in self.items:
            price = self.item_frozen_price(item) if self.order.is_paid else self.item_live_price(item)
            total += price * item.count
        return total

    # تخفیف حاصل از کد تخفیف
    def discount_amount(self):
        d = self.order.discount_code
        if not d or d.is_expired() or d.discount_amount <= 0:
            return 0
        return d.discount_amount

    # مجموع پس از تخفیف کد
    def total_after_discount(self):
        return max(0, self.items_total() - self.discount_amount())

    # مجموع + هزینه ارسال
    def total_with_shipping(self):
        return self.total_after_discount() + self.order.shipping

    # قیمت خام بدون هیچ تخفیفی
    def regular_total(self):
        total = 0
        for item in self.items:
            total += item.product.price * item.count
        return total

    # مقدار تخفیف محصول (تخفیف درصدی)
    def product_discount_amount(self):
        total = 0
        for item in self.items:
            raw = item.product.price
            live = item.product.final_price
            total += (raw - live) * item.count
        return total

    # تخفیف کلی: تخفیف محصول + تخفیف کد تخفیف
    def full_discount(self):
        return self.product_discount_amount() + self.discount_amount()

    # تولید کد رهگیری
    def generate_tracking_code(self):
        while True:
            code = str(secrets.randbelow(900000) + 100000)
            from order.models import Order
            if not Order.objects.filter(tracking_code=code).exists():
                return code
