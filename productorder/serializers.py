from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Order, Address, ProductOder, Payment
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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['type', 'timestamp']

class OrderSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    address = AddressSerializer(required=False, allow_null=True)
    payment = PaymentSerializer(required=False, allow_null=True)
    class Meta:
        model = Order
        fields = [
            'id',
            'reference',
            'checked',
            'date',
            'user',
            'products',
            'amount',
            'address',
            'payment'
        ]
        extra_kwargs = {
            # 'id': {'read_only': True},
            'checked': {'read_only': True},
            'reference': {'read_only': True}
        }

    def get_products(self, obj):

        serializer_products = ProductOrderSerializer(obj.products, many=True)
        return serializer_products.data


class ProductOrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(default=1)


class CreateOrderSerializer(serializers.Serializer):
    products = ProductOrderItemSerializer(many=True)
    coupon = serializers.CharField(max_length=20, required=False, allow_blank=True)



