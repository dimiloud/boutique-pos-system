from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = ['total']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date', 'payment_method', 'total']
    list_filter = ['payment_method', 'date']
    search_fields = ['id', 'customer__first_name', 'customer__last_name']
    inlines = [SaleItemInline]
    readonly_fields = ['subtotal', 'tax', 'total']
    fieldsets = [
        ('Informations de base', {
            'fields': ['customer', 'payment_method']
        }),
        ('Montants', {
            'fields': ['subtotal', 'tax', 'total']
        }),
        ('Notes', {
            'fields': ['notes']
        }),
    ]