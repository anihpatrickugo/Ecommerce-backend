from django.db import models
from django.contrib.auth import get_user_model

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

from products.models import  Products
# Create your models here.

User = get_user_model()


class ProductOder(models.Model):

    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} order"

    @property
    def price(self):
        return self.product.price * self.quantity


class Address(models.Model):
    zip = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = CountryField()
    phone = PhoneNumberField()

class Payment(models.Model):
    payment_choices = (
        ('stripe', 'STRIPE'),
        ('paypal', 'PAYPAL')
    )
    reference = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=payment_choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class OrderCoupon(models.Model):
    name = models.CharField(max_length=20, unique=True)
    discount = models.IntegerField()
    created = models.DateField(auto_now_add=True)
    expires = models.DateField()

    def __str__(self):
        return  self.name



class Order(models.Model):
    products = models.ManyToManyField(ProductOder)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=12, blank=True, unique=True)
    checked = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    # coupon = models.ForeignKey(OrderCoupon, on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(Address, on_delete=models.CASCADE,
                                   blank=True, null=True)
    coupon = models.ForeignKey(OrderCoupon, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} order'

    @property
    def amount(self):
        total = 0

        for product in self.products.all():
            total += product.price

        if self.coupon:
            discount_price = (self.coupon.discount/100) * total
            final_price = total -discount_price
            return final_price

        else:
            return total






