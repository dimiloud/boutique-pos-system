from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'loyalty_points', 'active']
    list_filter = ['active']
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = [
        ('Informations personnelles', {
            'fields': ['first_name', 'last_name', 'email', 'phone', 'address']
        }),
        ('Fidélité', {
            'fields': ['loyalty_points']
        }),
        ('Statut', {
            'fields': ['active', 'notes', 'created_at', 'updated_at']
        }),
    ]