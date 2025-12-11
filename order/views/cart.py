from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from product.models import Product
from order.models import Order, OrderItems
from django.contrib.auth.decorators import login_required


@ratelimit(key='ip', rate='25/m', method='POST', block=True)
@require_POST
@login_required
def add_product_to_cart(request):
    try:
        product_id = int(request.POST.get('product_id'))
        count = int(request.POST.get('count', 1))
    except (ValueError, TypeError):
        return JsonResponse({
            "status": "invalid_input",
            "text": "مقدار وارد شده معتبر نیست",
            "icon": "warning",
        })

    if count < 1:
        return JsonResponse({
            "status": "invalid_count",
            "text": "تعداد باید حداقل ۱ باشد",
            "icon": "warning",
        })

    product = Product.objects.filter(id=product_id, is_active=True, is_stock=True).first()
    if not product:
        return JsonResponse({
            "status": "not_found",
            "text": "محصول مورد نظر یافت نشد",
            "icon": "error",
        })

    if product.stock < count:
        return JsonResponse({
            "status": "out_of_stock",
            "text": "موجودی محصول کافی نیست",
            "icon": "warning",
        })

    try:
        with transaction.atomic():
            order, created = Order.objects.get_or_create(user=request.user, is_paid=False)

            order_item, item_created = OrderItems.objects.get_or_create(
                order=order,
                product=product,
                defaults={'unit_price': product.price, 'count': 0}
            )
            order_item.count += count
            order_item.unit_price = product.price
            order_item.save()

        from order.utils import OrderCalculator
        calculator = OrderCalculator(order)
        total_price = calculator.total_with_shipping()
        total_discount = calculator.full_discount()

        return JsonResponse({
            "status": "success",
            "text": "محصول با موفقیت به سبد خرید اضافه شد",
            "icon": "success",
            "cart": {
                "total_price": total_price,
                "total_discount": total_discount,
                "item_count": order.items.count()
            }
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "text": f"خطای سرور: {str(e)}",
            "icon": "error",
        })
