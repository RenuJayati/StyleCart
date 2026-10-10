from django.contrib import admin
from .models import Product, Order, ContactMessage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'mobile',
        'city',
        'total_amount',
        'created_at'
    )

    search_fields = (
        'customer_name',
        'mobile',
        'city'
    )

    list_filter = ('city', 'created_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)