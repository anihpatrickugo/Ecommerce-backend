from rest_framework import generics
from rest_framework import mixins

from .models import Products, Categories
from .serializers import ProductSerializer, CategoriesSerializer
from . import mixins

# Create your views here.

class ProductView(mixins.GetMethodListOrDetail, generics.GenericAPIView):
    """
    This is the view which list all available products and also
    enable the viewing of each product in detail
    """

    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    paginate_by = 1


class CategoryView(mixins.GetMethodListOrDetail, generics.GenericAPIView):

    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
