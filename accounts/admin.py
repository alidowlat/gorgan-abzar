from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'phone_number', 'email', 'first_name', 'last_name', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined', 'otp_create_at')
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Personal Information', {'fields': ('first_name', 'last_name')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('History', {'fields': ('last_login', 'date_joined', 'otp_create_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )
