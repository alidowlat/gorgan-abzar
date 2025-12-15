import json
from django.http import JsonResponse
from django.template.loader import render_to_string
from order.models import Order


class CartManager:
    def __init__(self, order):
        self.order = order

    @property
    def items(self):
        return self.order.items.select_related("product")

    def sync_prices(self):
        updated = False
        for item in self.items:
            new_price = item.product.final_price
            if item.unit_price != new_price:
                item.unit_price = new_price
                item.save()
                updated = True
        return updated

    def sync_with_stock(self):
        messages = []
        removed_items = []

        for item in self.items.select_related("product"):
            p = item.product

            if not p.is_active or p.stock <= 0:
                removed_items.append(item)
                messages.append(f"محصول «{p.title}» ناموجود یا غیرفعال شده")
                continue

            if item.count > p.stock:
                item.count = p.stock
                item.save()
                messages.append(
                    f"تعداد محصول «{p.title}» به حداکثر موجودی ({p.stock}) اصلاح شد"
                )

        for item in removed_items:
            item.delete()

        return {
            "messages": messages,
            "removed": bool(removed_items),
        }

    def calculate(self):
        stock_result = self.sync_with_stock()
        total_before = 0
        total_after = 0
        total_items = 0
        total_profit = 0
        output_items = []

        for item in self.items:
            p = item.product
            total_before += p.price * item.count
            total_after += item.unit_price * item.count
            total_items += item.count

            raw_total = p.price * item.count
            final_total = item.unit_price * item.count

            # total_before += raw_total
            # total_after += final_total
            # total_items += item.count

            profit = raw_total - final_total
            total_profit += profit

            output_items.append({
                "id": item.id,
                "product": p,
                "product_id": p.id,
                "title": p.title,
                "image": p.image.url if p.image else None,
                "count": item.count,
                "unit_price": item.unit_price,
                "raw_unit_price": p.price,
                "raw_total_price": raw_total,
                "total_price": final_total,
                "profit": profit,
                "stock": p.stock,
            })

        discount_amount = 0
        final_price = total_after
        if self.order.discount_code:
            discount_amount = self.order.discount_code.apply_discount(total_after)
            final_price -= discount_amount

        if self.order.discount_code:
            final_price = self.order.apply_discount(final_price)

        return {
            "items": output_items,
            "total_items": total_items,
            "total_before_discount": total_before,
            "total_after_discount": total_after,
            "discount_amount": discount_amount,
            "final_price": final_price,
            "total_profit": total_profit,
            "messages": stock_result["messages"],
        }

    def update_item(self, item_id, count):
        item = self.items.select_related("product").filter(id=item_id).first()
        if not item:
            return {"status": "error"}
        p = item.product
        if not p.is_active or p.stock <= 0:
            item.delete()
            return {
                "status": "removed",
                "message": f"محصول «{p.title}» ناموجود یا غیرفعال شده",
            }
        item.count = min(max(count, 1), p.stock)
        item.save()

        return {"status": "ok", "count": item.count}

    def remove_item(self, item_id):
        item = self.items.filter(id=item_id).first()
        if not item:
            return {"status": "error"}
        item.delete()
        return {"status": "ok", "order_deleted": not self.order.items.exists()}

    def clear_items(self):
        self.items.delete()
        return {"status": "ok", "order_deleted": True}


class CartAction:
    def __init__(self, request):
        self.request = request
        self.order = Order.objects.filter(user=request.user, is_paid=False).first()
        self.manager = CartManager(self.order) if self.order else None
        try:
            self.data = json.loads(request.body)
        except Exception:
            self.data = {}

    def get_item_id(self):
        item_id = self.data.get('item_id')
        try:
            return int(item_id)
        except (TypeError, ValueError):
            return None

    def get_count(self):
        return int(self.data.get('count', 1))

    def render_response(self, result):
        if not self.order or not self.manager:
            return JsonResponse({'status': 'order_not_found'})

        self.order.refresh_from_db()

        cart_data = self.manager.calculate()
        body = render_to_string('order/cart/content.html', {
            'order': self.order,
            'items': cart_data['items'],
            'total_items': cart_data['total_items'],
            'total_before_discount': cart_data['total_before_discount'],
            'total_after': cart_data['total_after_discount'],
            'discount_amount': cart_data['discount_amount'],
            'final_price': cart_data['final_price'],
            'total_profit': cart_data['total_profit'],
        })
        item_id = self.get_item_id()
        item_total = 0
        item_raw = 0
        for i in cart_data['items']:
            if i['id'] == item_id:
                item_total = i['total_price']
                item_raw = i['raw_total_price']

        return JsonResponse({
            **result,
            'body': body,
            'item_total': item_total,
            'item_raw': item_raw,
            'discount_amount': cart_data['discount_amount'],
            'total_before_discount': cart_data['total_before_discount'],
            'final_price': cart_data['final_price'],
            'total_profit': cart_data['total_profit'],
        })
