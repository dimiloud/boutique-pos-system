from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sku', 'barcode', 'size', 'color', 'price', 'stock_quantity', 'active']
    list_filter = ['category', 'size', 'color', 'active']
    search_fields = ['name', 'sku', 'barcode']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Informations de base', {
            'fields': ['name', 'category', 'description']
        }),
        ('Caractéristiques', {
            'fields': ['sku', 'barcode', 'size', 'color']
        }),
        ('Prix et stock', {
            'fields': ['price', 'cost_price', 'stock_quantity', 'alert_quantity']
        }),
        ('Statut', {
            'fields': ['active', 'created_at', 'updated_at']
        }),
    ]