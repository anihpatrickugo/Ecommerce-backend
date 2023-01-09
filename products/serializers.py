from rest_framework import serializers

from .models import Products, Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['pk', 'name']



class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        # categories = CategoriesSerializer(read_only=True)

        model = Products
        fields = [
            'id',
            'url',
            'image',
            'name',
            'initial_price',
            'price',
            'description',
            'categories',
            'discount'
        ]


