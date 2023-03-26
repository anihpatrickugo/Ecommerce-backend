from rest_framework import serializers

from .models import Products, Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name']





class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategoriesSerializer(many=True)

    class Meta:

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



