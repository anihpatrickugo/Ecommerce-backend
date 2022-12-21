from django.db import models
from django.contrib.auth import get_user_model

from products.models import  Products
# Create your models here.

User = get_user_model()

class ProductOder(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} order"

class Order(models.Model):
    products = models.ManyToManyField(ProductOder)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)