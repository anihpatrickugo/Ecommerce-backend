import logging

from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    paginate_by = 1

    # this is not part of the parent class attributes
    logger.info('getting all products')



class CategoryView(mixins.GetMethodListOrDetail, generics.GenericAPIView):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # this is not part of the parent class attributes
    logger.info('getting a product instance')
