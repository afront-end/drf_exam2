from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'selling_price', 'purchase_price', 'added_by', 'created_at')
    list_filter = ('created_at', 'added_by')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'photo')
        }),
        ('Цены', {
            'fields': ('purchase_price', 'selling_price')
        }),
        ('Метаданные', {
            'fields': ('added_by', 'created_at', 'updated_at')
        }),
    )