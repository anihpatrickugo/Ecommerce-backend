from django.contrib import admin

from .models import ProductOder, Order

# Register your models here.

@admin.register(ProductOder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'user']
    list_filter = ['product', 'user']


@admin.register(Order)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'id']
    list_filter = ['products', 'user', 'date']