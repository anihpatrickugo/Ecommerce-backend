from django.contrib import admin

from .models import ProductOder, Address, Order

# Register your models here.


@admin.register(ProductOder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'user', 'id']
    list_filter = ['product', 'user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['order', 'zip', 'district', 'city', 'state', 'country', 'phone']
    # list_filter = []


@admin.register(Order)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'id']
    list_filter = ['products', 'user', 'date']