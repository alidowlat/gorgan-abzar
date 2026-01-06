from django.contrib import admin

from contact.models import ContactUs


class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone_number', 'subject', 'message', 'created_at']


admin.site.register(ContactUs, ContactAdmin)
