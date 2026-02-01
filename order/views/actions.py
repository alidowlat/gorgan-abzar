import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django_ratelimit.decorators import ratelimit
from order.utils import OrderCalculator, CartAction
from product.models import Product
from order.models import Order, OrderItems
from django.contrib.auth.decorators import login_required


@ratelimit(key='ip', rate='25/m', method='POST', block=True)
@require_POST
@login_required
def add_product_to_cart(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status": "invalid_json",
            "text": "فرمت داده صحیح نیست",
            "icon": "warning",
        })

    try:
        product_id = int(data.get("product_id"))
        count = int(data.get("count", 1))
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

    order = Order.objects.filter(user=request.user, is_paid=False).first()

    current_count = 0
    if order:
        existing_item = OrderItems.objects.filter(
            order=order,
            product=product
        ).first()
        if existing_item:
            current_count = existing_item.count

    if product.stock < count:
        return JsonResponse({
            "status": "out_of_stock",
            "text": f"موجودی محصول کافی نیست ({product.stock} عدد موجود است)",
            "icon": "warning",
        })

    if current_count + count > product.stock:
        return JsonResponse({
            "status": "max_stock_reached",
            "text": f"شما از حداکثر موجودی این کالا ({product.stock} عدد) در سبد خریدتان دارید",
            "icon": "warning",
        })

    try:
        with transaction.atomic():
            order, created = Order.objects.get_or_create(
                user=request.user,
                is_paid=False
            )

            order_item, item_created = OrderItems.objects.get_or_create(
                order=order,
                product=product,
                defaults={
                    'unit_price': product.final_price,
                    'count': 0
                }
            )

            order_item.count += count
            order_item.unit_price = product.final_price
            order_item.save()

        calculator = OrderCalculator(order)

        return JsonResponse({
            "status": "success",
            "text": "محصول با موفقیت به سبد خرید اضافه شد",
            "icon": "success",
            "cart": {
                "total_price": calculator.total_with_shipping(),
                "total_discount": calculator.full_discount(),
                "item_count": order.items.count()
            }
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "text": f"خطای سرور: {str(e)}",
            "icon": "error",
        })


def need_login():
    return JsonResponse({
        "status": "login_required",
        "icon": "warning",
        "text": "برای انجام این عملیات ابتدا وارد حساب کاربری شوید"
    })


@require_POST
def product_add(request):
    if not request.user.is_authenticated:
        return need_login()
    data = json.loads(request.body)
    product_id = data.get("product_id")
    count = int(data.get("count", 1))
    product = Product.objects.filter(id=product_id).first()
    if not product:
        return JsonResponse({"status": "not_found", "icon": "error", "text": "محصول پیدا نشد"})
    order, _ = Order.objects.get_or_create(user=request.user, is_paid=False)
    item, _ = OrderItems.objects.get_or_create(order=order, product=product)
    item.count += count
    item.save()
    return JsonResponse({"status": "ok", "icon": "success", "text": "به سبد خرید اضافه شد"})


@require_POST
@login_required
def cart_update(request):
    base = CartAction(request)
    if not base.order:
        return JsonResponse({'status': 'order_not_found'})

    item_id = base.get_item_id()
    count = base.get_count()
    result = base.manager.update_item(item_id, count)
    return base.render_response(result)


@require_POST
@login_required
def cart_remove(request):
    base = CartAction(request)
    if not base.order:
        return JsonResponse({'status': 'order_not_found'})

    item_id = base.get_item_id()
    result = base.manager.remove_item(item_id)
    return base.render_response(result)


@require_POST
@login_required
def cart_clear(request):
    base = CartAction(request)
    if not base.order:
        return JsonResponse({'status': 'order_not_found'})

    result = base.manager.clear_items()
    return base.render_response(result)
