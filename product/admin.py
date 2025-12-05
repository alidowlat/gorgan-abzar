from django.contrib import admin
from product.models import Product, ProductCategory, Brand, Feature, Gallery


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1
    min_num = 0
    max_num = 20


class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1
    min_num = 1
    max_num = 30


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_rate', 'final_price', 'category', 'brand', 'is_active', 'featured']
    list_filter = ['is_active', 'featured', 'category', 'brand']
    search_fields = ['title', 'slug']
    inlines = [FeatureInline, GalleryInline]
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Information', {
            'fields': ('title', 'slug', 'image', 'guarantee','description')
        }),
        ('Price', {
            'fields': ('price', 'discount_rate')
        }),
        ('Categories', {
            'fields': ('category', 'brand')
        }),
        ('Status', {
            'fields': ('is_active', 'is_stock', 'stock', 'featured')
        }),
        ('Time Since..', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProductCategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'slug']
    prepopulated_fields = {"slug": ("title_en",)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_filter = ['is_active']
    search_fields = ['title', 'slug']
    prepopulated_fields = {"slug": ("title_en",)}


@admin.register(Feature)
class FeaturesAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value']
    search_fields = ['product__title', 'key', 'value']


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    search_fields = ['product__title']
    list_filter = ['product']
