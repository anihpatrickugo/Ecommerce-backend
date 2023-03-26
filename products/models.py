from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return  self.name


class Products(models.Model):
    image = models.ImageField(upload_to='products')
    name  = models.CharField(max_length=40)
    initial_price = models.IntegerField()
    description = models.TextField()
    categories = models.ManyToManyField(Categories)
    discount = models.IntegerField(blank=True, null=True)
    date_added = models.DateField(auto_now_add=True)


    def __str__(self):
        return  self.name

    @property
    def price(self):
        if self.discount:
            discounted = ( self.discount /100) * self.initial_price
            new_price = self.initial_price - discounted
            return new_price
        return self.initial_price

