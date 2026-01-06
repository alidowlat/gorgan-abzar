from django.contrib import admin

from order.models import DiscountCode, DiscountCodeUser, OrderItems, Order


class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0
    readonly_fields = ('created_at',)
    autocomplete_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'status',
        'is_paid',
        'tracking_code',
        'paid_at',
        'created_at',
    )
    list_filter = (
        'status',
        'is_paid',
        'created_at',
    )
    search_fields = (
        'id',
        'tracking_code',
        'user__phone_number',
        'user__first_name',
        'user__last_name',
    )
    readonly_fields = (
        'tracking_code',
        'paid_at',
        'created_at',
        'updated_at',
    )
    list_select_related = ('user',)
    inlines = (OrderItemsInline,)
    ordering = ('-created_at',)
    actions = ('mark_as_shipped', 'mark_as_delivered')

    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')


@admin.register(OrderItems)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'count',
        'unit_price',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = (
        'order__id',
        'product__title',
    )
    autocomplete_fields = ('order', 'product')


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_amount',
        'expiration_date',
        'is_expired',
    )
    list_filter = ('expiration_date',)
    search_fields = ('code',)
    readonly_fields = ()
    ordering = ('-expiration_date',)


@admin.register(DiscountCodeUser)
class DiscountCodeUserAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'discount_code',
        'is_paid',
        'used_at',
    )
    list_filter = (
        'is_paid',
        'used_at',
    )
    search_fields = (
        'user__phone_number',
        'discount_code__code',
    )
    autocomplete_fields = ('user', 'discount_code')