from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, UserAddress
from core.models import Settings


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'phone_number', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined', 'otp_created_at')
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('History', {'fields': ('last_login', 'date_joined', 'otp_created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "state",
        "city",
        "is_default",
        "created_at",
    )
    list_filter = (
        "is_default",
        "state",
        "city",
        "created_at",
    )
    search_fields = (
        "full_name",
        "phone_number",
        "postal_code",
        "full_address",
        "user__phone_number",
        "user__email",
    )
    ordering = (
        "-is_default",
        "-created_at",
    )
    raw_id_fields = (
        "user",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (None, {
            "fields": (
                "user",
                "is_default",
            )
        }),
        ("User Information", {
            "fields": (
                "full_name",
                "phone_number",
            )
        }),
        ("Address Information", {
            "fields": (
                "state",
                "city",
                "postal_code",
                "plaque",
                "full_address",
            )
        }),
        ("Date and Time", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


admin.site.register(Settings)
