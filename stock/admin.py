from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'quantity', 'updated_at')
    list_filter = ('product', 'size')
    search_fields = ('product__name',)
    readonly_fields = ('updated_at',)
    ordering = ('product', 'size')