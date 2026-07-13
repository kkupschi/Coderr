from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_user', 'business_user', 'status', 'created_at']
    list_filter = ['status', 'offer_type']
