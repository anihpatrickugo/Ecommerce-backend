from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import  Response

from. models import Order, ProductOder
from products.models import Products
from .serializers import OrderSerializer, CreateOrderSerializer

# Create your views here.


class CartView( mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    This view bring the current cart which has not been checked.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return: the cart currently been used
        """
        user = self.request.user
        order = Order.objects.filter(user=user, checked=False)
        if order.exists():
            cart = order.last()
            serializer = OrderSerializer(cart)
            return Response(serializer.data)


class OrdersView( mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    This view return the list of all orders by a user and also creates order for a user
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs) -> Response:
        """

        :param request:
        :param args:
        :param kwargs:
        :return: response with the list of orders.
        """
        return self.list(request)

    def post(self, request, *args, **kwargs) -> Response:
        """

        :param request:
        :param args:
        :param kwargs:
        :return: response with the order instance created.
        """
        user = self.request.user
        serializer = CreateOrderSerializer(data=self.request.data, many=True)
        order_instance = Order.objects.create(user=user)

        if serializer.is_valid(raise_exception=True):
            products = serializer.validated_data

            for product in products:
                product_id = product.get('id')
                product_instance = Products.objects.get(id=product_id)
                product_quantity = product.get('quantity')

                product_order = ProductOder.objects.create(user=user,
                                                           product=product_instance,
                                                           quantity=product_quantity)
                product_order.save()
                order_instance.products.add(product_order)

        order_serializer = OrderSerializer(order_instance)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    # def put(self, request, *args, **kwargs) -> Response:
    #     user = self.request.user
    #     id = kwargs.get('id')
    #     order = get_object_or_404(Order, user=user, id=id)
    #
    #     if order is not None:
    #         serializer = CreateOrderSerializer(data=self.request.data, many=True)
    #
    #         if serializer.is_valid(raise_exception=True):
    #             products = serializer.validated_data
    #             clear_products = order.products.clear()
    #
    #             for product in products:
    #                 product_id = product.get('id')
    #                 product_instance = Products.objects.get(id=product_id)
    #                 product_quantity = product.get('quantity')
    #
    #                 product_order = ProductOder.objects.create(user=user,
    #                                                            product=product_instance,
    #                                                            quantity=product_quantity)
    #                 product_order.save()
    #                 order.products.add(product_order)
    #
    #         order_serializer = OrderSerializer(order)
    #         return Response(order_serializer.data, status=status.HTTP_200_OK)
    #
    #     return Response({'message': 'order instance not found'},
    #                     status=status.HTTP_404_NOT_FOUND)

    def get_queryset(self) -> queryset:
        """

        :return: A queryset of orders by the request user.
        """

        user = self.request.user
        qs = Order.objects.filter(user=user)
        return qs
