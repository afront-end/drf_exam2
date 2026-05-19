from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'customer', 'seller', 'size', 'quantity', 'price', 'payment_method', 'created_at')
    list_filter = ('payment_method', 'created_at', 'seller')
    search_fields = ('product__name', 'customer__username', 'seller__username')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    raw_id_fields = ('product', 'customer', 'seller')