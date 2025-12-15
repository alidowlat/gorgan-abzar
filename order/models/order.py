from django.db import models

ORDER_STATUS_STYLES = {
    'cart': {'color': 'text-yellow-500'},
    'pending': {'color': 'text-blue-500'},
    'shipped': {'color': 'text-green-600'},
    'delivered': {'color': 'text-blue-500'},
}


class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'در انتظار پرداخت'),
        ('pending', 'پردازش و بسته بندی'),
        ('shipped', 'ارسال شده'),
        ('delivered', 'تحویل داده شده'),
    ]
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
    )
    shipping = models.PositiveIntegerField(
        default=0,
    )
    tracking_code = models.CharField(
        max_length=16,
        unique=True,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='cart',
    )
    discount_code = models.ForeignKey(
        'order.DiscountCode',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    shipping_code = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(
        default=False
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def get_status_style(self):
        return ORDER_STATUS_STYLES.get(self.status, {})

    def get_total_price(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).items_total()

    def set_final_price(self):
        from order.utils import OrderCalculator
        self.final_price = OrderCalculator(self).total_with_shipping()

    def set_tracking_code(self):
        from order.utils import OrderCalculator
        self.tracking_code = OrderCalculator(self).generate_tracking_code()

    def __str__(self):
        return f'Order #{self.id} - {self.user} - {self.status}'

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'orders'


class OrderItems(models.Model):
    order = models.ForeignKey(
        'order.Order',
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'product.Product',
        models.CASCADE,
        related_name='order_items'
    )
    count = models.PositiveSmallIntegerField()
    unit_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def final_price(self):
        return self.unit_price * self.count

    @property
    def total(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).total_after_discount()

    @property
    def total_with_shipping(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).total_with_shipping()

    @property
    def discount_total(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).full_discount()

    @property
    def regular_total(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).regular_total()

    def generate_tracking_code(self):
        from order.utils import OrderCalculator
        return OrderCalculator(self).generate_tracking_code()

    def __str__(self):
        return f'OrderItem #{self.order_id} - {self.product}'

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'
        db_table = 'order_items'
