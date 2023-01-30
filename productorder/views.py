import logging
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import views
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import  Response

from products.models import Products

from. models import Order, ProductOder
from .permissions import IsOrderOwner
from .serializers import OrderSerializer, AddressSerializer, CreateOrderSerializer

logger = logging.getLogger('django.request')
# Create your views here.


class CartView( mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    This view bring the current cart which has not been checked.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

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
            logger.info('returning the current cart')
            return Response(serializer.data)


class OrdersView(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin, mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    """
    This view return the list of all orders by a user and also creates order for a user
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderOwner]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs) -> Response:
        """

        :param request:
        :param args:
        :param kwargs:
        :return: response with the list of orders.
        """
        order_id = kwargs.get('id')
        if order_id:
            logger.info('returning an order info')
            return self.retrieve(request, *args, **kwargs)

        logger.info('returning all orders by this user')
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
        logger.info('new order created')
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs) -> Response:
        # grab order details from request. r
        user = self.request.user
        order_id = kwargs.get('id')
        order = get_object_or_404(Order, user=user, id=int(order_id))

        # check if order exists in database
        if order is not None:
            serializer = CreateOrderSerializer(data=self.request.data, many=True)

            # check if serialized data is accepted
            if serializer.is_valid(raise_exception=True):
                products = serializer.validated_data

                # empty the previous order products
                for product in order.products.all():
                    id = product.id
                    product = ProductOder.objects.get(id=id)
                    product.delete()

                # add get all modified order products and add them
                for product in products:
                    product_id = product.get('id')

                    product_instance = Products.objects.get(id=product_id)
                    product_quantity = product.get('quantity')

                    product_order = ProductOder.objects.create(user=user,
                                                               product=product_instance,
                                                               quantity=product_quantity)
                    product_order.save()
                    order.products.add(product_order)

            order_serializer = OrderSerializer(order)
            logger.info('modified an order instance')
            return Response(order_serializer.data, status=status.HTTP_200_OK)

        logger.error('could not retrieve the order instance to be modified')
        return Response({'message': 'order instance not found'},
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs) -> Response:

        order_id = kwargs.get('id')
        user = self.request.user
        order = get_object_or_404(Order, user=user, id=int(order_id))
        order.delete()

        logger.info('deleted an order instance')
        return Response({'message': 'order deleted'},
                        status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self) -> queryset:
        """

        :return: A queryset of orders by the request user.
        """

        user = self.request.user
        qs = Order.objects.filter(user=user)
        return qs


class CheckoutView(views.APIView):
    """
    This view adds the destination address of the
    order.
    """

    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        data = self.request.data
        user = self.request.user
        order = get_object_or_404(Order, id=int(order_id), user=user)
        address_serializer = AddressSerializer(data=data)

        if address_serializer.is_valid(raise_exception=True):
            address = address_serializer.save()
            order.address = address
            order.save()

            logger.info('address info added to order')
            return Response({'message': 'address added successfully'},
                            status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        order_id = kwargs.get('id')
        data = self.request.data
        user = self.request.user
        order = get_object_or_404(Order, id=int(order_id), user=user)
        order_address = order.address
        address_serializer = AddressSerializer(data=data)

        if address_serializer.is_valid(raise_exception=True):
            address = address_serializer.update(instance=order_address,
                                                validated_data=address_serializer.data)
            order.address = address
            order.save()

            logger.info('order address info is modified')
            return Response({'message': 'address updated successfully'},
                            status=status.HTTP_201_CREATED)
