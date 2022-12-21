from django.contrib import admin

from .models import Products, Categories

# Register your models here.

@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']
    list_filter = ['name', 'price', 'description']

@admin.register(Categories)
class ProductAdmin(admin.ModelAdmin):
    pass