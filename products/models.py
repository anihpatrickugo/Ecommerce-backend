from django.db import models

# Create your models here.

class Categories(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return  self.name


class Products(models.Model):
    image = models.ImageField(upload_to='products')
    name  = models.CharField(max_length=40)
    price = models.IntegerField()
    description = models.TextField()
    categories = models.ManyToManyField(Categories)
    discount = models.DecimalField(decimal_places=2, max_digits=100.00, blank=True, null=True)


    def __str__(self):
        return  self.name

