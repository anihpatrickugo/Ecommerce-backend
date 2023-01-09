from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Order, ProductOder
from products.serializers import ProductSerializer



class ProductOrderSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()

    class Meta:

        model = ProductOder
        fields = [
            # 'id',
            'quantity',
            'product',
            'price'
        ]

        # extra_kwargs = {
        #     'id': {'read_only': True}
        #
        # }

    def get_product(self, obj):
        request = self.context.get('request')
        product = obj.product
        serializer = ProductSerializer(product, context={'request': request})

        id = serializer.data.get('id')
        name = serializer.data.get('name')
        price = serializer.data.get('price')
        image = serializer.data.get('image')

        return {
                   'id': id,
                   'name':name,
                   'price': price,
                   'image': image
        }




class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields =  [
            'id',
            'reference',
            'checked',
            'date',
            'user',
            'products'
        ]
        extra_kwargs = {
            # 'id': {'read_only': True},
            'checked': {'read_only': True},
            'reference': {'read_only': True}
        }

    def get_products(self, obj):

        serializers = ProductOrderSerializer(obj.products, many=True)
        return serializers.data


class CreateOrderSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1)