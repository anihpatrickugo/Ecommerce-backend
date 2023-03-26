import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination


from .models import Products, Categories
from .serializers import ProductSerializer, CategoriesSerializer
from . import mixins

logger = logging.getLogger('django.request')
# Create your views here.

class ProductView(mixins.GetMethodListOrDetail, generics.GenericAPIView):
    """
    This is the view which list all available products and also
    enable the viewing of each product in detail
    """

    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    # this is not part of the parent class attributes
    logger.info('getting all products')

    def get_queryset(self, *args, **kwargs):
        categories = self.request.query_params.get('categories')

        if categories:
            qs = super().get_queryset().filter(categories__name__icontains=categories)
        else:
            qs = super().get_queryset()

        return qs



class CategoryView(mixins.GetMethodListOrDetail, generics.GenericAPIView):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # this is not part of the parent class attributes
    logger.info('getting a product instance')

